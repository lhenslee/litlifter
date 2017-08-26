from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from . import views
from . import models

urlpatterns = [
    url(r'^$', models.index, name = 'index'),
    url(r'^profile/', models.configure, name = 'configure'),
    url(r'^login/', models.login, name = 'login'),
    url(r'^create/', models.CreateAccount, name = 'CreateAccount'),
]
