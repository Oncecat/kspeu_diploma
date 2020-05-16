from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls), # включить админку
    url(r'^$', views.iptable),
    path("", include("authentication.urls")),  
    path("", include("app.urls")),  
]
