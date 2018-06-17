from django.shortcuts import render
from wbuilder.views import initContent
import sys, os

def index(request):
    initContent()
    if request.session['member'] != None: return render('/login')
    return render(request, 'handmade/account.html')
