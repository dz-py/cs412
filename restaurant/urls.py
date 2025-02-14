# restaurant/urls.py
# This file defines the URL patterns for WcDonald's.
# It maps URLs to their corresponding views, such as the main page, order page, and confirmation page.

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.main, name='main_page'),
    path(r'main', views.main, name="main_page"),
    path(r'order', views.order, name="order_page"),
    path(r'confirmation', views.confirmation, name="confirmation_page"),
]

