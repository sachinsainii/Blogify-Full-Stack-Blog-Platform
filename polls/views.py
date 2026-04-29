from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now())
        order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'
    # def get_queryset(self):
    #     return Question.objects.filter(pub_date__lte=timezone.now())
   

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'
    def results(request, question_id):
       question = get_object_or_404(Question, pk=question_id)
       return render(request, 'results.html', {'question': question})
   

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html',{
            'question': question,
            'error_message': "you didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        