from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, Item_Image, Watch_List
from django.views import generic
from users.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory, modelformset_factory
from .decorators import active_auction

from operator import attrgetter
from django.db.models import Q
from .forms import *
# Create your views here.


# def is_valid_queryparam(param):
#     return param != '' and param is not None


class ItemListView(generic.ListView):
    model = Item
    template_name = 'bazaar/home.html' # <APP>/<MODEL>_<VIEWTYPE>.HTML
    context_object_name = 'posts'  # def: home
    ordering = '-date_posted'
    paginate_by = 4

    def get_queryset(self):
        queryset = Item.objects.all().order_by('-date_posted')
        title_contains_query = self.request.GET.get('title_contains')
        if title_contains_query != '' and title_contains_query is not None:
            queryset = queryset.filter(Q(title__icontains=title_contains_query)).order_by('-date_posted')
        return queryset


class MerchantItemListView(generic.ListView):
    model = Item
    template_name = 'bazaar/merchant_items.html' # <APP>/<MODEL>_<VIEWTYPE>.HTML
    context_object_name = 'posts'  # def: home
    ordering = '-date_posted'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Item.objects.filter(merchant=user).order_by('-date_posted')


class MerchantBidListView(generic.ListView):
    model = Bid
    template_name = 'bazaar/merchant_bids.html' # <APP>/<MODEL>_<VIEWTYPE>.HTML
    context_object_name = 'bids'  # def: home
    paginate_by = 15

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        # item = Item.objects.filter(merchant=user)
        return Bid.objects.filter(merchant=user).order_by('-date')


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'bazaar/item_detail.html'

    def get_queryset(self):
        return Item.objects.filter(date_posted__lte=timezone.now())


def item_detail(request, slug=None):
    item = get_object_or_404(Item, slug=slug)
    item_images = list(Item_Image.objects.filter(item=item))

    context = {
        'item': item,
        'images': item_images,
        'bids': Bid.objects.filter(item=item).order_by('-date')
    }
    return render(request, "bazaar/item_detail.html", context)


class ItemCreateView(LoginRequiredMixin, generic.CreateView):  # this order redirect to login page if you're not logged
    model = Item
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.merchant = self.request.user
        return super().form_valid(form)


@active_auction
@login_required
def bidding(request, slug):
    item = get_object_or_404(Item, slug=slug)
    form = BiddingForm(request.POST, old_price=item.price)
    if request.method == "POST":
        if form.is_valid():  # This would call the clean method for you
            bid = form.save(commit=False)
            bid.item = item
            bid.merchant = request.user
            bid.save()
            item.price = bid.bid
            item.save()
            messages.success(request, "Auction has been successfully bidded.")
            return HttpResponseRedirect(item.get_absolute_url())
        else:  # Form is invalid
            print
            form.errors  # You have the error list here.

    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'bazaar/bidding.html', context)


@login_required
def item_create(request):
    ImageFormset = modelformset_factory(Item_Image, fields=('image',), extra=4, max_num=5)
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES)
        # datetime_form = ItemCreateDatetimeForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.merchant = request.user
            item.save()
            for f in formset:
                try:
                    photo = Item_Image(item=item, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            messages.success(request, "Post has been successfully created.")
            return HttpResponseRedirect(item.get_absolute_url())
    else:
        form = ItemCreateForm()
        formset = ImageFormset(queryset=Item_Image.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'bazaar/item_create.html', context)


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

