from sqlite3 import IntegrityError
from django.shortcuts import render
from .forms import SignupForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login ,logout


def signup(request):
    if request.user.is_authenticated:
        return redirect('polls:index')
    if request.method == "GET":
        form = SignupForm()
        return render(request, 'user/signup.html', {'form': form})
    else:
        form = SignupForm(request.POST)

    if form.is_valid():
        try:
            user = User()
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']
            user.email = form.data['email']
            user.username = form.data['email']
            user.password = make_password(form.data['password'])
            user.save()
            login(request, user)
            return redirect('/polls/')
        except IntegrityError as e:
            return render(request, 'user/signup.html', {'form': form, 'errors': "Username already exists"})
    else:
        return render(request, 'user/signup.html', {'form': form, 'errors': "Invalid data"})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('polls:index')
    if request.method =="GET":
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    if user:
        login(request, user)
        return redirect("polls:index")
    else:
        form = LoginForm()
        return redirect("/login/", {'form': form, 'errors': "Credentials Incorrect"})

def logout_view(request):
    logout(request)
    return redirect('/login/')

