from django.shortcuts import render
from Users.models import UserProfile,UserProfileInfo
from followers.models import Followers
from Comments.models import Comment
from FollowCategory.models import CategoryFollowers
from Likes.models import CardLikes
from journal.models import Journal
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    context = {}
    if str(request.user) != 'AnonymousUser':
        user = request.user
        user = UserProfile.objects.get(user=user)
        context = {'user': user}
    else:
        request.user = None
        context = {'user': request.user}

    return render(request, "home.html", context)


def save_profile(backend, response,user=None, *args, **kwargs):
    import ipdb; ipdb.set_trace()
    if backend.name == 'facebook':
        
        if not UserProfile.objects.filter(user=user).exists():
            profile = User.objects.get(username=user)
            
            email = response.get('email')
            uname=str(profile)
            user_info=UserProfile(user=profile,name=uname,email=email)
            user_info.save()
            user_profile_info=UserProfileInfo(userlink=user_info)
            user_profile_info.save()
            user_followers_info = Followers(user=user_info)
            user_followers_info.save()
            user_comment_info = Comment(user=user_profile_info)
            user_comment_info.save()
            user_cat_info = CategoryFollowers(user=user_info)
            user_cat_info.save()
            user_like_info = CardLikes(user=user_info)
            user_like_info.save()
            user__jour_info = Journal(user=user_info)
            user__jour_info.save()


    elif backend.name == "google-oauth2":
        if not UserProfile.objects.filter(user=user).exists():
            profile = User.objects.get(username=user)
            
            email = response.get('emails')
            email= email[0].get('value')
            uname=str(profile)
            user_info=UserProfile(user=profile,name=uname,email=email)
            user_info.save()
            user_profile_info=UserProfileInfo(userlink=user_info)
            user_profile_info.save()
            user_followers_info = Followers(user=user_info)
            user_followers_info.save()
            user_comment_info = Comment(user=user_profile_info)
            user_comment_info.save()
            user_cat_info = CategoryFollowers(user=user_info)
            user_cat_info.save()
            user_like_info = CardLikes(user=user_info)
            user_like_info.save()
            user__jour_info = Journal(user=user_info)
            user__jour_info.save()