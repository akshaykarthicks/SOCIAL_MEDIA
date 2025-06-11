from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid #to generate the unique id for the post
from datetime import datetime


User=get_user_model() #to get the user model for the project

# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) #to delete the user profile if the user is deleted
    id_user=models.IntegerField() #to store the user id
    bio=models.TextField(blank=True) #to store the user bio
    profileimg=models.ImageField(upload_to='profile_images',default='blank-profile-picture.png') #image field is used to upload images to the database
    location=models.CharField(max_length=100,blank=True) #to store the user location
    
    
    def __str__(self):
        return self.user.username #to return the user username  
    
class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False) #to generate the unique id for the post
    user=models.CharField(max_length=100) #to store the user name
    image=models.ImageField(upload_to='post_images') #image field is used to upload images to the database
    caption=models.TextField(blank=True) 
    created_At=models.DateTimeField(auto_now_add=True) 
    no_of_likes=models.IntegerField(default=0)
    
    
    def __str__(self):  
        return self.user #to return the post caption
    
    
# to store the like post 
class LikePost(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

#followers
class FollowersCount(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)
    
    def __str__(self):
        return self.follower