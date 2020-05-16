from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls), # включить админку
    url('ui-tables.html', views.iptable),
    path("authentication/", include("authentication.urls")),  
    path("", include("app.urls")),  
]
