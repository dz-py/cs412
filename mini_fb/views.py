# mini_fb/views.py
# define views for the mini_fb app
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateProfileStatusForm
from django.contrib.auth.mixins import LoginRequiredMixin

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

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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
        # Save the status message to database
        sm = form.save()
        # Read the files from the form
        files = self.request.FILES.getlist('files')
        # Process each uploaded file
        for file in files:
            # Create a new Image object
            image = Image(
                profile=profile,
                image_file=file
            )
            image.save()
            status_image = StatusImage(
                status_message=sm,
                image=image
            )
            status_image.save()
        
        # Call parent method to finish the creation
        return super().form_valid(form)

    
    def get_success_url(self):
        '''Return a URL to which we should be directed after the form is successfully submitted'''
        # Get the pk of the profile that this status message is for
        profile_pk = self.kwargs['pk']
        # Reverse to profile page for this profile
        return reverse('show_profile', kwargs={'pk': profile_pk})

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' Define a view class that updates a profile '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    ''' Define a view class that deletes a status message '''
    model = StatusMessage
    context_object_name = 'status_message'
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        # Return url after successful delete
        profile = self.object.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    ''' Define a view class that updates a status message '''
    model = StatusMessage
    context_object_name = 'status_message'
    template_name = 'mini_fb/update_status_form.html'
    form_class = UpdateProfileStatusForm

    def get_success_url(self):
        # Return url after successful update
        profile = self.object.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})

class CreateFriendView(LoginRequiredMixin, View):
    '''Define a view class that creates a friend relationship between two profiles'''
    
    def dispatch(self, request, *args, **kwargs):
        '''Process the request to add a friend relationship'''
        # get the profile doing the friending (current user profile)
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        
        # get the profile to add as a friend
        other_pk = self.kwargs['other_pk']
        other_profile = Profile.objects.get(pk=other_pk)
        
        # add the friend relationship
        profile.add_friend(other_profile)
        
        # redirect back to the current user's profile page after done adding friend
        return redirect(reverse('show_profile', kwargs={'pk': profile_pk}))
    

class ShowFriendSuggestionsView(DetailView):
    ''' Define a view class that shows friend suggestions for a profile '''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

class ShowNewsFeedView(DetailView):
    """Display the news feed for a profile."""
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'