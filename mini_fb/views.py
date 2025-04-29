# mini_fb/views.py
#
# This file contains the views for the mini_fb app.
# It handles the logic for displaying pages and processing user input.

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateProfileStatusForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

    def get_context_data(self, **kwargs):
        '''Return a dictionary with context data for this template to use'''

        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        # Create an instance of UserCreationForm and add it to the context
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''Handle case when the form is valid'''
        # Reconstruct the UserCreationForm with POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Validate the user form
        if user_form.is_valid():
            # Save the user and get the User object
            user = user_form.save()
            
            # Log the user in
            login(self.request, user)
            
            # Attach the User to the Profile instance
            form.instance.user = user
        
        # Delegate to the superclass method to complete the process
        return super().form_valid(form)


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    ''' Define a view class that creates a new status message '''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_object(self):
        '''Get the profile for the logged-in user'''
        try:
            # Find the profile associated with the logged-in user
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            # If no profile exists for the user, raise a permission denied error
            raise PermissionDenied("You must create a profile first.")
    
    def get_context_data(self, **kwargs):
        '''Return a dictionary with context data for this template to use'''
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        # Get the profile for the logged-in user
        profile = self.get_object()
        # Add this profile to the context
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''Handle case when the form is valid'''
        # Get the profile for the logged-in user
        profile = self.get_object()
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
        # Get the profile for the logged-in user
        profile = self.get_object()
        # Reverse to profile page for this profile
        return reverse('show_profile', kwargs={'pk': profile.pk})

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' Define a view class that updates a profile '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        '''Get the profile for the logged-in user'''
        try:
            # Find the profile associated with the logged-in user
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            # If no profile exists for the user, raise a permission denied error
            raise PermissionDenied("You must create a profile first.")

    def get_success_url(self):
        '''Return URL after successful update'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

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
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            raise PermissionDenied("You must create a profile first.")
        
        # get the profile to add as a friend
        other_pk = self.kwargs['other_pk']
        other_profile = Profile.objects.get(pk=other_pk)
        
        # add the friend relationship
        profile.add_friend(other_profile)
        
        # redirect back to the current user's profile page after done adding friend
        return redirect(reverse('show_profile', kwargs={'pk': profile.pk}))
    

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' Define a view class that shows friend suggestions for a profile '''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Get the profile for the logged-in user'''
        try:
            # Find the profile associated with the logged-in user
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            # If no profile exists for the user, raise a permission denied error
            raise PermissionDenied("You must create a profile first.")

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """Display the news feed for a profile."""
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Get the profile for the logged-in user'''
        try:
            # Find the profile associated with the logged-in user
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            # If no profile exists for the user, raise a permission denied error
            raise PermissionDenied("You must create a profile first.")