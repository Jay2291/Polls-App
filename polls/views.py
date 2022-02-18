from pyexpat.errors import messages
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Choice, Question
from user.forms import QuestionForm
from django.shortcuts import redirect

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.all()


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required()
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def add_question(request):
    if request.method == "GET":
        form = QuestionForm()
        return render(request, 'polls/add_question.html', {'form': form})
    else:
        form = QuestionForm(request.POST)
        choices = request.POST.getlist('q_choices')
        if form.is_valid():
            f = form.save()
            choice_list = []
            for choice in choices:
                choice_list.append(Choice(choice_text=choice, question_id=f.id))
            Choice.objects.bulk_create(choice_list)
            messages.success(request, 'Question Added Successfully.')
            return redirect('polls:index')
        else:
            form1 = QuestionForm()
            return render(request, 'polls/add_question.html', {'form': form1, 'errors': form.errors})


