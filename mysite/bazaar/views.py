from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, Item_Image
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import *
# Create your views here.

def home(request):
    context = {
        'posts': Item.objects.all()  # wrong name, shoudl be items
    }
    return render(request, 'bazaar/home.html', context)

class ItemListView(generic.ListView):
    model = Item
    template_name = 'bazaar/home.html' # <APP>/<MODEL>_<VIEWTYPE>.HTML
    context_object_name = 'posts'  # def: home
    ordering = '-date_posted'
    paginate_by = 3

class MerchantItemListView(generic.ListView):
    model = Item
    template_name = 'bazaar/merchant_items.html' # <APP>/<MODEL>_<VIEWTYPE>.HTML
    context_object_name = 'posts'  # def: home
    ordering = '-date_posted'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Item.objects.filter(merchant=user).order_by('-date_posted')

class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'bazaar/item_detail.html'
    # context_object_name = 'latest_question_list'
    # def get_queryset(self):
    #     """
    #     Return the last five published questions (not including those set to be
    #     published in the future).
    #     """
    #     # lte- less then or equal to
    #     return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Item.objects.filter(date_posted__lte=timezone.now())

class ItemCreateView(LoginRequiredMixin, generic.CreateView):  # this order redirect to login page if you're not logged
    model = Item
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.merchant = self.request.user
        return super().form_valid(form)

# class Item_ImageCreateView(Item, LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
#     model = Item_Image
#     fields = ['name', 'image']
#
#     def form_valid(self, form):
#         form.instance.item = Item
#         return super().form_valid(form)
#
#
#     def test_func(self):
#         item_image = self.get_object()
#         if self.request.item == item_image.item:
#             return True
#         return False

@login_required
def item_create(request):
    ImageFormset = modelformset_factory(Item_Image, fields=('image',), extra=3)
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES)
        formset = ImageFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.merchant = request.user
            item.save()

            for f in formset:
                try:
                    photo = Item_Image(item=item, image=f.cleaned_data.get('image'))
                    photo.save()
                except Exception as e:
                    break
            messages.success(request, "Post has been successfully created.")
            return HttpResponseRedirect('/item/%s/' %item.id)
        else:
            return redirect('bazaar-about')
    else:
        form = ItemCreateForm()
        formset = ImageFormset(queryset=Item_Image.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'bazaar/item_create.html', context)



# class Item_ImageUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
#     model = Item_Image
#     fields = ['name', 'image']
#
#     def form_valid(self, form):
#         form.instance.item = Item
#         return super().form_valid(form)
#
#     def test_func(self):
#         item = self.get_object()
#         if self.request.item == item.merchant:
#             return True
#         return False

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Item
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.merchant = self.request.user
        return super().form_valid(form)
# check correctness login with owner of item
    def test_func(self):
        item = self.get_object()
        if self.request.user == item.merchant:
            return True
        return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):  # this order redirect to login page if you're not logged
    model = Item
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.merchant:
            return True
        return False

def about(request):
    return render(request, 'bazaar/about.html', {'title': 'about'})

# def edit_item(request, item_id):
#     question = get_object_or_404(Question, pk = item_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
#     else:
#         selected_choice.votes +=1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#     return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
