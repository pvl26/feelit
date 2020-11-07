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
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    current_moods = models.JSONField(default=default_moods)
    goal_moods = models.JSONField(default=default_moods)
    email = models.EmailField(default=None);
    phone = models.CharField(max_length=10, default=None)
    website = models.CharField(max_length=100, default=None)
    twitter = models.CharField(max_length=100, default=None)
    instagram = models.CharField(max_length=100, default=None)
    facebook = models.CharField(max_length=100, default=None)
    description = models.TextField(default="About Me")


    def __str__(self):
        return f'{self.user.username} Profile'



