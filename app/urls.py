from django.urls import path, re_path
from app import views
# from django.conf.urls import url 

urlpatterns = [
    # Matches any html file
    path('ui-tables.html', views.iptable),
    
    path('detail/<str:slug>/', views.iptable_detail, name='ip_detail'),
    path('ui-sysinfo.html',views.sysinfo),
    re_path(r'^.*\.html', views.pages, name='pages'),
    # The home page
    path('', views.index, name='home'),

]
