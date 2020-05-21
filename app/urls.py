from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file
    path('', views.iptable),
    path('detail/<str:slug>/', views.iptable_detail, name='ip_detail'),
    re_path(r'^.*\.html', views.pages, name='pages'),
    # The home page
    path('', views.index, name='home'),

]
