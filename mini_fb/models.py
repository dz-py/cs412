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
    
    def get_friends(self):
        ''' Return a list of friend's profiles '''
        # find all Friend objects where this profile is either profile1 or profile2
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        
        # create a list of the friend's profiles
        friend_profiles = []
        for friend in friends_as_profile1:
            friend_profiles.append(friend.profile2)
        for friend in friends_as_profile2:
            friend_profiles.append(friend.profile1)
        
        return friend_profiles
    
    def add_friend(self, other):
        '''Add a friend relationship between profiles if not already exists'''
        # can't friend yourself
        if self == other:
            return None
        
        # check if friendship already exists in either direction
        existing = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | 
            models.Q(profile1=other, profile2=self)
        ).first()
        
        if existing:
            return existing
        
        # create new friendship
        friendship = Friend(profile1=self, profile2=other)
        friendship.save()
        return friendship
    
    def get_friend_suggestions(self):
        ''' Return a list of profiles that could be suggested as friends '''
        current_friends = self.get_friends()
        
        # get all profiles except self
        all_other_profiles = Profile.objects.exclude(pk=self.pk)
        
        # filter out profiles that are already friends
        suggestions = [profile for profile in all_other_profiles if profile not in current_friends]
        
        return suggestions
    
    def get_news_feed(self):
        """
        Return all status messages from this profile and all of its friends,
        ordered by timestamp with the most recent first.
        """
        # get friends of this profile
        friends = self.get_friends()
        
        # add self to the list of profiles whose messages we want
        profiles = [self] + friends
        
        # get all status messages from these profiles
        news_feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
        
        return news_feed
    
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
    

class Friend(models.Model):
    ''' Encapsulates the idea of an edge connecting two nodes within the social network '''

    # define the fields of the friend model
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ''' Return a string representation of the friend model '''
        return f'{self.profile1} & {self.profile2}'
