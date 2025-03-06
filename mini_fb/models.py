# mini_fb/models.py
# define data models for the mini_fb app
from django.db import models
from django.urls import reverse
                  
# Create your models here.
class Profile(models.Model):
    ''' Encapsulate the data of a user profile '''

    # define the fields of the profile
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    address = models.TextField(blank=True)
    # profile image is just a www url to the image
    profile_image = models.TextField(blank=True)

    def __str__(self):
        ''' Return a string representation of the profile '''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        ''' Return the status messages of this profile and order them by timestamp '''
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        ''' Return a URL to display this profile object '''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    ''' Encapsulate the data of a status message '''

    # define the fields of the status message 
    timestamp = models.DateTimeField(auto_now_add=True) 
    message = models.TextField(blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        ''' Return a string representation of the status message '''
        return f'{self.timestamp} {self.message}'
    
    def get_images(self):
        ''' Return all images associated with this status message '''
        # get all StatusImage objects that reference this status message
        status_images = StatusImage.objects.filter(status_message=self)
        # extract the related Image objects
        images = [status_image.image for status_image in status_images]
        return images
    
class Image(models.Model):
    ''' Encapsulate the data of an image '''

    # define the fields of the image
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        ''' Return a string representation of the image '''
        return f'{self.image_file}'

class StatusImage(models.Model):
    ''' Encapsulate the data of a status image '''

    # define the fields of the status image
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        ''' Return a string representation of the status image '''
        return f'StatusImage: {self.status_message} - {self.image}'
    