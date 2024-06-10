from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields here

    def __str__(self):
        return self.user.username
    
class Club(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='clubs')
    logo = models.ImageField(upload_to='media/', default='joker.png.jpg')

    def __str__(self):
        return self.name