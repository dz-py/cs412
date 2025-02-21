# mini_fb/views.py
# define views for the mini_fb app
from django.shortcuts import render
from django.views.generic import ListView, DetailView # a list of all instances of a model
from .models import Profile

# Create your views here.
class ShowAllProfilesView(ListView):
    ''' Define a view class that shows all profiles '''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    ''' Define a view class that shows a single profile '''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'