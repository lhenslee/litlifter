from django.shortcuts import render
import sys, os

def index(request):
    if request.session['member'] != None: return render('/login')
    return render(request, 'membership/index.html')
