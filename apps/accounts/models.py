from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def default_moods():
    return {'happy':'50',
            'hopeful':'50',
            'adventure':'50',
            'chill':'50',
            'dreamy':'50',
            'sad':'50',
     }

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default=None, blank=True)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    current_moods = models.JSONField(default=default_moods)
    goal_moods = models.JSONField(default=default_moods)
    email = models.EmailField(default=None, blank=True)
    phone = models.CharField(max_length=10, default=None, blank=True)
    website = models.CharField(max_length=100, default=None, blank=True)
    twitter = models.CharField(max_length=100, default=None, blank=True)
    instagram = models.CharField(max_length=100, default=None, blank=True)
    facebook = models.CharField(max_length=100, default=None, blank=True)
    description = models.TextField(default="About Me")


    def __str__(self):
        return f'{self.user.username} Profile'



class Person(models.Model):
    avatar = models.ImageField("avatar", upload_to="avatars")

    def __unicode__(self):
        return self.name