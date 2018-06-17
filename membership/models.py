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
    user = Account.objects.get(username=request.session['member'])
    content['profile'] = user.username
    content['email'] = user.email
    content['difficulty'] = user.experience
    content['equipment'] = user.equipment
except Exception as e: pass

# Create a new account
def CreateAccount(request):
    # Initialize content
    content['username'] = 'Username - 6+'
    content['email'] = 'Email address'
    content['email2'] = 'Repeat email address'
    content['password'] = 'Password - 6+'
    content['password2'] = 'Repeat Password'

    # Respond to submission
    if request.method == "POST": 
        ''' Create a new account if...
        - Username is more than 5 in length
        - Both passwords match
        - Email does not exist
        - Both emails pass
        - The user does not exist already
        If successful go to the home page
        '''
        if (len(request.POST['username']) > 5 and request.POST['email']==request.POST['email2']
            and len(request.POST['password']) > 5 and request.POST['password']==request.POST['password2']
            and not Account.objects.filter(username=request.POST['username'])):
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            request.session['username'] = username
            item = Account.objects.create(username=username,email=email,password=password,
                experience=request.POST['Experience'],equipment=','.join(request.POST.getlist('Equipment')))
            request.session['member'] = username
            return HttpResponseRedirect('/')

        # Store attempts into placeholder
        content['username'] = request.POST['username']
        content['email'] = request.POST['email']
        content['email2'] = request.POST['email2']
        content['password'] = request.POST['password']
        content['password2'] = request.POST['password2']
        
        # User already exists error
        if (Account.objects.filter(username=request.POST['username'])):
            content['username'] = 'This username is taken.'

        # Emails do not match
        if (request.POST['email']!=request.POST['email2']):
            content['email2'] = 'The emails do not match.'

        # No username present
        if (not request.POST['username']):
            content['username'] = 'Please input a username.'

        # Improper email format
        if ('@' not in request.POST['email']):
            content['email'] = 'Improper email format.'

        # Passwords do not match
        if (request.POST['password'] != request.POST['password2']):
            content['password2'] = 'The passwords do not match.'

        # Password is too short
        if (len(request.POST['password']) < 6):
            content['password'] = 'The password must have 6 or more.'
            content['password2'] = 'Password is too short'
    return render(request, 'handmade/signup.html', content)

# Login page
def login(request):
    # Handle login submission
    if request.method == "POST": 
        content['username_attempt'] = 'Username or email'
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
            return render(request, 'handmade/login.html', login_page)
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
    if request.method == "POST":
        if request.POST['submission'] == 'Submit':
            if request.POST['Difficulty'] != 'Select Difficulty':
                Account.objects.filter(username=request.session['member']).update(
                    experience=request.POST['Difficulty'])
            Account.objects.filter(username=request.session['member']).update(
                equipment=','.join(request.POST.getlist('Equipment')))
                
        if request.POST['submission'] == 'Logout':
            request.session['member'] = ''
            return HttpResponseRedirect('/')
    try:
        content['profile'] = request.session['member'].capitalize()
        content['signup'] = ''
    except Exception as e: pass
    return render(request, 'handmade/account.html', content)



        
