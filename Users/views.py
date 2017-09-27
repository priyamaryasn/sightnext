from django.shortcuts import render_to_response, HttpResponseRedirect, render, get_object_or_404
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.context_processors import csrf
from .models import UserProfile, UserProfileInfo
from .forms import UserProfileInfoForm
from django.http import Http404
from followers.models import Followers
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from Blogs.models import Cards
from FollowCategory.models import CategoryFollowers
from Comments.models import Comment
from followers.models import Followers
from categories.models import Categories
from Likes.models import CardLikes
from journal.models import Journal

# Create your views here.


def register(request):
    context = {}
    #import ipdb; ipdb.set_trace()

    if request.method == 'POST':
        try:
            name = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password2 == password1:
                user = User.objects.create_user(
                    username=name,
                    password=password1,
                    email=email)
                user_info = UserProfile(user=user, name=name, email=email)
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
                name = request.POST.get("username")
                password = request.POST.get("password1")
                user = auth.authenticate(username=name, password=password)
                if request.user.is_authenticated():
                    context = {"status": "One user already logged in"}
                    context['user'] = request.user.username
                    context.update(csrf(request))
                    return render_to_response("login.html", context)
                else:
                    if user is not None:
                        if user.is_active:
                            auth.login(request, user)
                      
                

                context = {'success': True, 'message': 'User Profile Created Successfully. Please tell us something about yourself.'}
                context.update(csrf(request))
                return HttpResponseRedirect("/users/userdetailsentry/%s/"%request.user)
        except:
            context = {'success': False, 'message': "user Profile can't be saved. please SignUp again"}
            context.update(csrf(request))
            return render_to_response("login.html", context)
    context.update(csrf(request))
    return render_to_response('login.html', context)


def login(request):
    context = {}
    #import ipdb; ipdb.set_trace()
    if request.method == "GET":
        if request.user.is_authenticated():
            context['user'] = request.user.username
            context.update(csrf(request))
            return render_to_response("login.html", context)
        else:
            context.update(csrf(request))
            return render_to_response("login.html", context)

    elif request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=name, password=password)
        if request.user.is_authenticated():
            context = {"status": "One user already logged in"}
            context['user'] = request.user.username
            context.update(csrf(request))
            return render_to_response("login.html", context)
        else:
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    context = {"status": "login successfull"}
                    
                    context={'user':request.user.username}
                    context.update(csrf(request))
                    return HttpResponseRedirect('/')
                else:
                    context = {"status": 'account de-activated'}
                    context.update(csrf(request))
                    return render_to_response("login.html", context)
            else:
                context = {"status": "invalid login details"}
                context.update(csrf(request))
                return render_to_response("login.html", context)
    else:

        context.update(csrf(request))
        return render_to_response("login.html", context)


@login_required(login_url='/users/login/')
def logout(request):
    # import ipdb; ipdb.set_trace()
    """Logout method for LoggedIn Users."""
    if request.user.is_authenticated():
        auth.logout(request)
        context = {}
        context['status'] = 'Logout sucessfull'
        context.update(csrf(request))
        return HttpResponseRedirect("/")
    else:
        pass


def home(request):
    context = {}

    return render(request, "about.html", context)


def about(request):
    context = {}

    return render(request, "about.html", context)


def contact(request):
    context = {}

    return render(request, "contact.html", context)

@login_required(login_url='/users/login/')
def user_details_entry1(request):
    # import ipdb; ipdb.set_trace()
    title = "Please fill this form so that everybody can know about you."
    if request.method=="POST":
        form = UserProfileInfoForm(request.POST, request.FILES or None)
        context = {
            'title': title,
            'form': form
        }
        user = request.user
        user = UserProfile.objects.get(user=user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.userlink = user
            instance.save()
            context = {
                'title': "thank you"
            }
        context.update(csrf(request))
        return HttpResponseRedirect("/users/%s"%str(request.user))
    else:
        form = UserProfileInfoForm(request.POST, request.FILES or None)
        context = {
            'title': title,
            'form': form
        }
    context.update(csrf(request))
    return render(request, 'userdetailsentry.html', context)
@login_required(login_url='/users/login/')
def user_details_entry(request):
    # import ipdb; ipdb.set_trace()
    
    context = {}
    if request.method == "POST":
        try:
            full_name = request.POST.get("full_name")
            pic = request.FILES.get("pic")
            sex = request.POST.get("sex")
            user = request.user
            user = UserProfile.objects.get(user=user)

            
            user = UserProfileInfo(
                userlink=user,
                full_name=full_name,
                gender=sex,
                profile_pic=pic)
            user.save()
            context = {
                "status": True, 'message': "Profile Saved."
            }
            context.update(csrf(request))
            return render_to_response("userdetailsentry.html", context)
        except:
            context = {
                "status": False, 'message': "Profile Not Saved."
            }
            context.update(csrf(request))
            return render_to_response("userdetailsentry.html", context)
    else:        
        user = request.user
        user = UserProfile.objects.get(user=user)
        if UserProfileInfo.objects.filter(userlink=user).exists():
            user = UserProfileInfo.objects.get(userlink=user)
            
            context={
                'user':user,
               
            }
            context.update(csrf(request))
            return render(request,"user.html", context)
        else:
            context={
            "title":"please fill the form below"
            }
            context.update(csrf(request))
            return render_to_response("userdetailsentry.html", context)
    context = {'message': "not saved"}
    context.update(csrf(request))
    return render_to_response("userdetailsentry.html", context)



def user(request, username):
    #import ipdb; ipdb.set_trace()

    if str(request.user) != "AnonymousUser":
        visitor = request.user
        visitor=UserProfile.objects.get(user=visitor)
        user = username
        user_name = UserProfile.objects.get(name=user)
        user = UserProfile.objects.get(name=user)
        cards = Cards.objects.all()
        user_cat=CategoryFollowers.objects.get(user=user_name)
        user_cat=user_cat.cat.all()
        cats = Categories.objects.all()[0:7]
        user_followers=Followers.objects.get(user=user_name)
        user_followers = user_followers.followed_by.all()
        user_journal = Journal.objects.get(user=user_name)
        show_cards=[]
        for card in cards:
            if card.user.name == username:
                
                show_cards.append(card)
        #user_followed= Followers.objects.get(user=user)
        #user_following=request.user
        #user_following = UserProfile.objects.get(name=user_following)
        
        username = UserProfile.objects.get(name=user)
        if UserProfileInfo.objects.filter(userlink=user).exists():
            
            user = UserProfileInfo.objects.get(userlink=user)
            if user_name.follower.filter(followed_by=visitor).exists():
                follow_button = "unfollow"
                
            else:
                follow_button = "follow"
            #if user_followed.objects.filter(followed_by=user_following).exists():
            
            context = {
                    'user': user,
                    'username':username,
                    'user_name':user_name,
                    "follow_button": follow_button,
                    "cards":show_cards,
                    "user_cat":user_cat,
                    "user_followers":user_followers,
                    "cats":cats,
                    'visitor':visitor,

            }
            context.update(csrf(request))
            return render(request, "user.html", context)
        else:
            title = "we dont know anything about you. please fill the details form"
            context = {'title': title}
    else:

        user = username
        user_name = UserProfile.objects.get(name=user)
        user = UserProfile.objects.get(name=user)
        cards = Cards.objects.all()
        user_cat=CategoryFollowers.objects.get(user=user_name)
        user_cat=user_cat.cat.all()
        user_followers=Followers.objects.get(user=user_name)
        user_followers = user_followers.followed_by.all()
        cats = Categories.objects.all()[0:7]
        show_cards=[]
        for card in cards:
            if card.user.name == username:
                
                show_cards.append(card)
        #user_followed= Followers.objects.get(user=user)
        #user_following=request.user
        #user_following = UserProfile.objects.get(name=user_following)
        
        username = UserProfile.objects.get(name=user)
        if UserProfileInfo.objects.filter(userlink=user).exists():
            
            user = UserProfileInfo.objects.get(userlink=user)
            follow_button = "follow"
            #if user_followed.objects.filter(followed_by=user_following).exists():
            
            context = {
                    'user': user,
                    'username':username,
                    "follow_button": follow_button,
                    "cards":show_cards,
                    "user_cat":user_cat,
                    "user_followers":user_followers,
                    "cats":cats,
            }
            context.update(csrf(request))
            return render(request, "user.html", context)
        else:
            title = "we dont know anything about you. please fill the details form"
            context = {'title': title}

    context.update(csrf(request))
    return render(request, "userdetailsentry.html", context)





@login_required(login_url='users/login/')
def profile_edit(request,username):
    # import ipdb; ipdb.set_trace()
    title = "Let us know you a little"

    instance=get_object_or_404(User,username=username)
    instance = UserProfile.objects.get(user=instance)
    if UserProfileInfo.objects.filter(userlink=instance).exists():
        instance = UserProfileInfo.objects.get(userlink=instance)
        if request.method =="GET":
            form = UserProfileInfoForm(request.POST or None,request.FILES or None,instance=instance)
            context = {
                "title": title,
                "form": form,
                "instance":instance,
            }
            context.update(csrf(request))
            return render(request, "userdetailsentry.html",context)    
        else:

            user = request.user
            user = UserProfile.objects.get(user=user)
            form = UserProfileInfoForm(request.POST or None,request.FILES or None, instance=instance)
            if form.is_valid():
                instance = form.save(commit=False)
                
                instance.save()

            #print request.POST.get('full_name')
            #print request.POST.get('sex')
            context = {
                "instance":instance,
                "title": "thanks for telling us more about you.",
            }
            context.update(csrf(request))
            return HttpResponseRedirect("/users/%s/"%username)
    else:
        if request.method =="GET":
            form = UserProfileInfoForm(request.POST or None)
            context = {
                "title": "Please tell us something about you",
                "form": form,
                "instance":instance,
            }   
        else:
            user = request.user
            user = UserProfile.objects.get(user=user)
            form = UserProfileInfoForm(request.POST,request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.userlink=user
                instance.save()

             
            context = {
                "instance":instance,
                "title": "thanks for telling us more about you.",
            }
        context.update(csrf(request))
        return render(request, "userdetailsentry.html",context)

                
    context.update(csrf(request))
    return render(request, "user.html",context)

@login_required(login_url='users/login/')
def change_password(request,username):
    #import ipdb; ipdb.set_trace()
    if request.method == "GET":
        try:
            if str(username) == str(request.user.username):
                context={"message" : " Please fill the details below.","user":username}
                context.update(csrf(request))
                return render(request,"password_change.html",context)
            else:
                raise Http404
                context={} 
                context.update(csrf(request))
                return render(request,"password_change.html",conext)
        except:
            raise Http404
    else:
        user=User.objects.get(username=username)
        old_password = request.POST.get("old_password")
        new_password_1 = request.POST.get("new_password_1")
        new_password_2 = request.POST.get("new_password_2")
        user = auth.authenticate(username=username, password=old_password)
        
        if (user is not None) & (new_password_1==new_password_2):
            try:
                user.set_password(new_password_1)
                user.save()
                auth.login(request, user)

            except:
                context = {"message": "Something went wrong please try again."}
                context.update(csrf(request))
                return render(request,"password_change.html",context)
            user = UserProfile.objects.get(user=user)
            user = UserProfileInfo.objects.get(userlink=user)
            context={"message": "Password changed successfully","user":user}
            context.update(csrf(request))
            return HttpResponseRedirect("/users/%s/"%request.user)
        else:
            if (user is not None) :
                context={"message": "Password did not match.. please fill again"}
            else:
                context={"message": "Current Password did not match"}
            context.update(csrf(request))
            return render(request,"password_change.html",context)





        