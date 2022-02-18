from django import forms
from django.forms import ModelForm
from polls.models import Question
from django.forms import widgets



class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(max_length=20, min_length=8)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=20, min_length=8)


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'pub_date': widgets.DateTimeInput(attrs={'type': 'date'}),
        }

