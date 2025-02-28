# mini_fb/views.py
# define views for the mini_fb app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm

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

class ShowStatusMessagesView(DetailView):
    ''' Define a view class that shows the status messages of a profile '''
    model = StatusMessage
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'messages'

class CreateProfileView(CreateView):
    ''' Define a view class that creates a new profile '''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    ''' Define a view class that creates a new status message '''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_context_data(self, **kwargs):
        '''Return a dictionary with context data for this template to use'''
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        # Get the profile that this status message is for
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        # Add this profile to the context
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''Handle case when the form is valid'''
        # Get the profile that this status message is for
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        # Associate this status message with this profile
        form.instance.profile = profile
        # Call parent method to finish the creation
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return a URL to which we should be directed after the form is successfully submitted'''
        # Get the pk of the profile that this status message is for
        profile_pk = self.kwargs['pk']
        # Reverse to profile page for this profile
        return reverse('show_profile', kwargs={'pk': profile_pk})