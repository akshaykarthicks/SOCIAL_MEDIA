from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile ,Post,LikePost,FollowersCount
from django.contrib.auth.decorators import login_required #only login and use the acc
from itertools import chain #to combine the list used for the feed
import random
import logging
logger = logging.getLogger(__name__)
# Create your views here.




@login_required(login_url='signin')  # only login and use the acc
def index(request):
    user_object=User.objects.get(username=request.user.username) #get the user object
    user_profile=Profile.objects.get(user=user_object) #get the user profile from the user to show in index heaader right
    
    
    #used to see other feed in the follwing feed 
    
    user_following_list=[]
    feed=[]
    
    user_following=FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
        
    #to get the feed from the user
    for username in user_following_list:
        feed_list=Post.objects.filter(user=username)
        feed.append(feed_list)
        
    feed_list= list(chain(*feed))
        
        
    
    # to show in post - get only one post
    #user suggestion
    all_users=User.objects.all()
    user_following_all=[]
    
    for user in user_following:
        user_list=User.objects.get(username=user.user)
    
    new_suggestion_list=[x for x in list(all_users) if (x not in list(user_following_all))]
    current_user=User.objects.get(username=request.user.username)  #self suggestion remove 
    final_suggestion_list=[x for x in list(new_suggestion_list) if (x != current_user)]
    random.shuffle(final_suggestion_list)
    
    username_profile=[]
    username_profile_list=[]
    
    for users in final_suggestion_list:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_lists=Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
        #to get the profile from the username from the profile model id
    suggestion_username_profile_list=list(chain(*username_profile_list))
    
    
    return render(request, 'index.html',{'user_profile':user_profile,'posts':feed_list,'suggestion_username_profile_list':suggestion_username_profile_list[:5]})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        email = request.POST['email']
        password = request.POST['password']
        password2= request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                logger.warning(f"Signup attempt failed: Email {email} already exists.")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                logger.warning(f"Signup attempt failed: Username {username} already exists.")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                
                # Attempt to authenticate the new user
                user_login = auth.authenticate(username=username, password=password)

                if user_login is not None:
                    auth.login(request, user_login)

                    #creating user for new user from the profile model
                    # to save the new user in the profile data base
                    user_model = User.objects.get(username=username) # Or directly use the 'user' object from create_user
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    logger.info(f"Account created successfully for username: {username}")

                    messages.success(request, 'Account created successfully and logged in!')
                    return redirect('index') # Redirect to index page
                else:
                    # This case should ideally not happen if create_user was successful
                    messages.error(request, 'Account created, but auto-login failed. Please try signing in.')
                    logger.error(f"Account created for {username}, but auto-login failed.")
                    return redirect('signin') # Redirect to signin page
            

        else:
            messages.error(request, 'Passwords do not match')
            logger.warning("Signup attempt failed: Passwords do not match.")
            return redirect('signup')   
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user=auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            logger.info(f"User {username} logged in successfully.")
            messages.success(request, 'Login Successful')               
            return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')
            logger.warning(f"Login attempt failed for username: {username}. Invalid credentials.")
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
    
@login_required(login_url='signin')  # only login and use the acc
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('signin')


# get the user profile from the profile model
@login_required(login_url='signin')  # only login and use the acc
def settings(request):
    user_profile=Profile.objects.get(user=request.user) #get the user profile
    if request.method=='POST':
        
        if request.FILES.get('image')== None: #no image selected
            image=user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']
            
            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
           
            
            user_profile.save()
            
        if request.FILES.get('image')!= None: #image selected
            image=request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']
           
            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            
            user_profile.save()
            
        return redirect('settings')
    
    return render(request, 'setting.html',{'user_profile':user_profile})



@login_required(login_url='signin') 
def upload(request):
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']
        
        new_post=Post.objects.create(user=user,image=image,caption=caption)  # new post upload 
        new_post.save()
        
        return redirect('index')
        
    else:
        return redirect('index')

# like post code - to store the like post
    
@login_required(login_url='signin')
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('id')
    
    post=Post.objects.get(id=post_id)  # to get the data from the post
    
    #already liked 
    like_filter=LikePost.objects.filter(username=username,post_id=post_id).first()
    
    
    if like_filter == None:
        new_like=LikePost.objects.create(username=username,post_id=post_id)
        new_like.save()
        
        #add likes to the post
        post.no_of_likes=post.no_of_likes+1
        post.save()
        
        return redirect('index')
    
    else:
        like_filter.delete()    
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('index')
        
    
    


#profile page

@login_required(login_url='signin')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    #get the user profile
    user_profile=Profile.objects.get(user=user_object)
    #get the no of posts
    user_posts=Post.objects.filter(user=pk)
    #get the no of posts
    user_post_length=len(user_posts)
    
    follower=request.user.username
    user=pk
    
    if FollowersCount.objects.filter(follower=follower,user=user).first():  #to check if the user is following the user
        button_text='Unfollow'
    else:
        button_text='Follow'
        
        
        #TO COUNT THE FOLLOWERS
    user_follower=len(FollowersCount.objects.filter(user=user))
    user_following=len(FollowersCount.objects.filter(follower=user))
    
    
    context={'user_profile':user_profile ,
             'user_object':user_object,
             'user_post_length':user_post_length,
             'user_posts':user_posts,
             'button_text':button_text,
             'user_follower':user_follower,
             'user_following':user_following
}
    
    
    return render(request, 'profile.html',context)

@login_required(login_url='signin')

def follow(request):
    if request.method=='POST':
        follower=request.POST['follower']
        user=request.POST['name']
        
        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowersCount.objects.filter(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)  #to redirect to the profile page
        else:
            new_follower=FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)  #to redirect to the profile page
    
    else:
        return redirect('index')

@login_required(login_url='signin')
    
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    if request.method=='POST':
        username=request.POST['username']
        username_object=User.objects.filter(username__icontains=username) #to search the username
        
        username_profile=[]
        username_profile_list=[]
        
        for users in username_object:
            username_profile.append(users.id)
        #to get the profile from the username from the profile model id
        for ids in username_profile:
            profile_lists=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
            
        username_profile_list=list(chain(*username_profile_list))    
    else:
        username_object = User.objects.none()
        username_profile_list = []
    return render(request, 'search.html',{'user_profile':user_profile,'username_object':username_object,'username_profile_list':username_profile_list})