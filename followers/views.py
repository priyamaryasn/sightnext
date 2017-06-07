from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from Users.models import UserProfile
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from followers.models import Followers
# Create your views here.

@login_required(login_url='users/login/')
def follow(request,username):
	if request.method == "POST":
		#import ipdb; ipdb.set_trace()
		context={}
		user_following =request.user
		user_following = UserProfile.objects.get(user = user_following)
		user_followed = User.objects.get(username=username)
		user_followed = UserProfile.objects.get(user = user_followed)
		try:
			if not Followers.objects.filter(user=user_following).exists():
				
				user = Followers(
					user=user_following,
					)
				user.save()
				user_following = Followers.objects.get(user=user_following)
				user_followed = Followers.objects.get(user=user_followed)
				user_following.follow.add(user_followed)
				message = "you are now following this user"
				if not Followers.objects.filter(user=user_followed).exists():
					user = Followers(
						user=user_followed,
						)
					user.save()
					user_followed = Followers.objects.get(user=user_followed)
					#user_following_1 = Followers.objects.get(user=user_following)
					user_followed.followed_by.add(user_following)
				else:
					user_followed = Followers.objects.get(user=user_followed)
					#user_following_1 = Followers.objects.get(user=user_following)
					user_followed.followed_by.add(user_following)
			else:
				
				if user_following.follower.filter(follows=user_followed).exists():
					user_following_1=Followers.objects.get(user=user_following)
					#user_followed_1 = Followers.objects.get(user=user_followed)
					user_following_1.follows.remove(user_followed)
					message="user unfollowed"
				else:
					user_following_1=Followers.objects.get(user=user_following)
					#user_followed_1 = Followers.objects.get(user=user_followed)
					user_following_1.follows.add(user_followed)
					message = "you are now following this user"
				if not Followers.objects.filter(user=user_followed).exists():
					user = Followers(
						user=user_followed,
						)
					user.save()
					user_followed = Followers.objects.get(user=user_followed)
					#user_following_1 = Followers.objects.get(user=user_following)
					user_followed.followed_by.add(user_following)
				else:
					
					if user_followed.follower.filter(followed_by=user_following).exists():
						user_followed_1=Followers.objects.get(user=user_followed)
						#user_following_1 = Followers.objects.get(user=user_following)
						user_followed_1.followed_by.remove(user_following)
						message=""
					else:
						user_followed_1=Followers.objects.get(user=user_followed)
						#user_following_1 = Followers.objects.get(user=user_following)
						user_followed_1.followed_by.add(user_following)
		except:
			message= "Something Bad Happened. Please try later..."



		#user_following = Followers.objects.get(user=user_following)
		#user_followed = User.objects.get(username=username)
		#user_followed = UserProfile.objects.get(user = user_followed)
		#user_followed = Followers.objects.get(user=user_followed)
		
		context = {
			"message": message,
			"followed":user_followed
		} 
		context.update(csrf(request))
		return HttpResponseRedirect("/users/%s/"%username)
	else:
		context={}
		context.update(csrf(request))
		return HttpResponseRedirect("/users/%s/"%username)

