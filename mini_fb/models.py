# mini_fb/models.py
# define data models for the mini_fb app
from django.db import models

# Create your models here.
class Profile(models.Model):
    ''' Encapsulate the data of a user profile '''

    # define the fields of the profile
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    address = models.TextField(blank=True)
    # profile image is just a www link to the image
    profile_image = models.TextField(blank=True)

