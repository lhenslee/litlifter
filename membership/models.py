from django.db import models
from django.shortcuts import render
from django.core import management
import sys, os
from django.core.cache import cache
from django.http import HttpResponseRedirect

class Account(models.Model):
    username = models.CharField(max_length=140)
    email = models.EmailField()
    password = models.CharField(max_length=140)
    experience = models.CharField(max_length=140)
    equipment = models.CharField(max_length=140)

    def __str__(self):
        return self.username
    
content = {}
content['password_attempt'] = 'Password'
content['username_attempt'] = 'Username or email'
content['profile'] = 'Login'
content['signup'] = 'Sign Up'
try:
    username = request.session['member']
    user = Account.objects.get(username=username)
    content['username'] = user.username
    content['email'] = user.email
    content['difficulty'] = user.experience
    content['equipment'] = user.equipment
except Exception as e: pass

def CreateAccount(request):
    if request.method == "POST": 
        print(request.POST)
    return render(request, 'handmade/signup.html', content)

def login(request):
    if request.method == "POST": 
        content['username_attempt'] = 'Username or email'
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        try:
            trial = Account.objects.get(username=username) 
            if password == trial.password:
                request.session['member'] = trial.username
                content['username'] = trial.username
                content['email'] = trial.email
                content['difficulty'] = trial.experience.capitalize()
                content['equipment'] = ', '.join(trial.equipment.split(','))
                return HttpResponseRedirect('/membership/profile')
            else:
                content['password_attempt'] = 'Invalid password.'
                print(content)
                return render(request, 'handmade/login.html', content)
        except Exception as e:
            content['username_attempt'] = username.capitalize() + ' does not exist.'
            print(content)
            return render(request, 'handmade/login.html', content)
    return render(request, 'handmade/login.html', content)
    try:
        request.session['member']
        return HttpResponseRedirect('/membership/profile')
    except Exception as e: return render(request, 'handmade/login.html', content)


def index(request):
    errors = {}
    login_page = {}
    try:
        user = request.session['member']
        login_page['username'] = user.username
        login_page['email'] = user.email
        print(login_page)
        if request.session['member'] != '':
            return render(request, 'membership/login.html', login_page)
    except Exception as e: print(e)
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        try:
            trial = Account.objects.get(username=username) 
            print(trial.username)
            if password == trial.password:
                request.session['member'] = trial.username
                login_page['username'] = trial.username
                login_page['email'] = trial.email
                login_page['difficulty'] = trial.experience.capitalize()
                login_page['equipment'] = ', '.join(trial.equipment.split(','))
                return render(request, 'handmade/login.html', login_page)
            else:
                content['password_attempt'] = 'Invalid password.'
                print(errors)
                return render(request, 'handmade/login.html', errors)
        except Exception as e:
            errors['invalid_user'] = username.capitalize() + ' does not exist.'
            print(errors)
            return render(request, 'membership/index.html', errors)
    return render(request, 'handmade/login.html')

def configure(request):
    return render(request, 'membership/login.html', content)



        
