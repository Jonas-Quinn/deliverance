from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from django.views import generic

# Create your views here.
class ItemView(generic.ListView):
    model = Item
    template_name = 'bazaar/item.html'
    # context_object_name = 'latest_question_list'
    # def get_queryset(self):
    #     """
    #     Return the last five published questions (not including those set to be
    #     published in the future).
    #     """
    #     # lte- less then or equal to
    #     return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

def home(request):
    context = {
        'posts': Item.objects.all()
    }
    return render(request, 'bazaar/home.html', context)


def about(request):
    return render(request, 'bazaar/about.html', {'title': 'about'})


def edit_item(request, item_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
