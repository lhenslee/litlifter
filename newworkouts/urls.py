from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from newworkouts.models import Post_workout

urlpatterns =[
    url(r'^$', ListView.as_view(queryset = Post_workout.objects.all().order_by("-rating"),
                                template_name='newworkouts/database.html')),
]
