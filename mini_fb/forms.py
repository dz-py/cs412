# mini_fb/forms.py
# defining forms, handling user input and data processing
from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' Define a form for creating a profile '''
    
    first_name = forms.CharField(label="First Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)
    city = forms.CharField(label="City", required=False)
    email = forms.CharField(label="Email", required=False)
    address = forms.CharField(label="Address", required=False)
    profile_image = forms.CharField(label="Profile Image URL", required=False)

    class Meta:
        ''' Define the model and fields for the form '''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'address', 'profile_image']

class CreateStatusMessageForm(forms.ModelForm):
    ''' Define a form for creating a status message '''
    
    message = forms.CharField(label="What's on your mind?", widget=forms.Textarea(attrs={'rows': 3}), required=True)
    
    class Meta:
        ''' Define the model and fields for the form'''
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    ''' Define a form for updating a profile '''
    
    city = forms.CharField(label="City", required=False)
    email = forms.CharField(label="Email", required=False)
    address = forms.CharField(label="Address", required=False)
    profile_image = forms.CharField(label="Profile Image URL", required=False)

    class Meta:
        ''' Define the model and fields for the form '''
        model = Profile
        fields = ['city', 'email', 'address', 'profile_image']