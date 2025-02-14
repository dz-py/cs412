from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.quote, name='home'),
    path(r'quote', views.quote, name='quote_page'),
    path(r'show_all', views.show_all, name='show_all_page'),
    path(r'about', views.about, name='about_page'),
]

