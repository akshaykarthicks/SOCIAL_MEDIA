from django.contrib import admin
from .models import Profile ,Post,LikePost,FollowersCount    #to register the profile model in the admin panel


# Register your models here.
#this is going to be used to register the models in the admin panel
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)

