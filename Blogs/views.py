from django.shortcuts import HttpResponseRedirect, render, get_object_or_404,redirect
from .models import Cards
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Users.models import UserProfile,UserProfileInfo
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from categories.models import Categories
from Comments.models import Comment
from Likes.models import CardLikes
from .forms import CardsForm
from FollowCategory.models import BlogsCategory
from journal.models import Journal

# Create your views here.


# @login_required(login_url="/users/login")
def all_cards(request):
    """This, function show all cards."""
    #import ipdb; ipdb.set_trace()
    cards = Cards.objects.all()
    cats=Categories.objects.all()[0:7]
    

    paginator = Paginator(cards, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        cards = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cards = paginator.page(paginator.num_pages)
    context = {
        'cards': cards,
        "cats":cats,
        "button_text": "button_text",
    }
    context.update(csrf(request))

    return render(request, "allcards.html", context)



def view_card(request, name):
    """For displaying single card."""
    #import ipdb; ipdb.set_trace()

    context = {}
    if str(request.user) != "AnonymousUser":
        user = request.user
        user = UserProfile.objects.get(name=user)
        card = get_object_or_404(Cards,slug=name)
        comment = card.name
        comment = Comment.objects.filter(comment_on_card=card)
       # comment_user = Comment.objects.get(comment_on_card=card)
        #user_info=UserProfileInfo.objects.get(userlink=comment_user.user)
        
        if (card.card_likes.filter(user=user).exists()):
            like_button = 'unlike'
        else:
            like_button = 'like'
        #users_journal=Journal.objects.get(user=user)
        user = UserProfile.objects.get(name=user)
        user_detail=UserProfileInfo.objects.get(userlink=user)
        if (user.my_journal.filter(collection=card).exists()):
            button_text= "delete from journal"
        else:
            button_text="add to journal"
        if card.v_type == "public":
            likers = []
            for item in CardLikes.objects.filter(like_on_card=card):
                likers.append(str(item.user))
            context = {
                'card': card,
                'like_button': like_button,
                'message': "public",
                "likers": likers,
                'comments': comment,
                "button_text": button_text,
                "user_d":user_detail,
                #"user_info":user_info,

            }
            context.update(csrf(request))
            return render(request, 'viewcard.html', context)
        else:
            if str(card.user) == str(request.user):
                context = {'message': "private", 'card': card}
                context.update(csrf(request))
                return render(request, 'viewcard.html', context)
            else:
                context = {'message': "Sorry. You are not authorised to see this card page."}
                context.update(csrf(request))
                return render(request, 'viewcard.html', context)
    else:
        user = request.user
        card = get_object_or_404(Cards,slug=name)
        comment = card.name
        comment = Comment.objects.filter(comment_on_card=card)
        like_button = 'like'
        button_text="add to journal"
        if card.v_type == "public":
            likers = []
            for item in CardLikes.objects.filter(like_on_card=card):
                likers.append(str(item.user))
            context = {
                'card': card,
                'like_button': like_button,
                'message': "public",
                "likers": likers,
                'comments': comment,
                "button_text": button_text,
                
                #"user_info":user_info,

            }
            context.update(csrf(request))
            return render(request, 'viewcard.html', context)
        else:
            if str(card.user) == str(request.user):
                context = {'message': "private", 'card': card}
                context.update(csrf(request))
                return render(request, 'viewcard.html', context)
            else:
                context = {'message': "Sorry. You are not authorised to see this card page."}
                context.update(csrf(request))
                return render(request, 'viewcard.html', context)


@login_required(login_url="/users/login/")
def new_card(request):
    #import ipdb; ipdb.set_trace()
    if request.method == "POST":

        context = {}
        
        form = CardsForm(request.POST, request.FILES or None)
        context = {
            "form": form,
            'message': "Please enter card information."

        }
        user = request.user
        user = UserProfile.objects.get(user=user)   

        if form.is_valid():
            instance = form.save( user)
            form.save_m2m()
            name=instance.slug
            context = {
                'message': "Card is Saved",
                
            }
            blog=Cards.objects.get(slug=name)
            for item in blog.blog_category.all():
                category_blog=Categories.objects.get(name=item)
                category_blog.blog_count+=1 
                category_blog.save()
                blog_category=BlogsCategory.objects.get(category=category_blog)
                blog_category.blogs.add(blog)


    else:
        
        context = {}
        # import ipdb; ipdb.set_trace()
        form = CardsForm()
        context = {
            "form": form,

            'message': "Please enter card information."

        }
        context.update(csrf(request))
        return render(request, "newcard.html", context)        

    context.update(csrf(request))
    return HttpResponseRedirect(instance.get_absolute_url())





def search(request):
   
    context = {}
    # import ipdb; ipdb.set_trace()

    if request.method == "POST":
        find = request.POST.get('find')
        cards = Cards.objects.filter(name__icontains=find)
        cats=Categories.objects.all()[0:5]
        
        context = {
            'list': cards,
            "cats":cats
        }
        context.update(csrf(request))

    return render(request, "show.html", context)


@login_required(login_url="/users/login/")
def edit_card(request,card_id):
    #import ipdb; ipdb.set_trace()
    instance=get_object_or_404(Cards,id=card_id)
    if Cards.objects.filter(id=card_id).exists():
        if request.method == "POST":
            context = {}
            instance=Cards.objects.get(id=card_id)
            form = CardsForm(request.POST or None, request.FILES or None, instance=instance)
            context = {
                "form": form,
                'message': "Please enter card information."

            }
            user = request.user
            user = UserProfile.objects.get(user=user)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                context = {
                    'message': "Card is Saved",
                    
                }
            else:
                context={
                    'message':"Please check the details entered by you."
                }
            context.update(csrf(request))
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            context = {}
            instance=Cards.objects.get(id=card_id)
            form = CardsForm(request.FILES or None,request.POST or None, instance=instance)
            context = {
                "form": form,
                'message': "Please enter card information."

            }
            user = request.user
            user = UserProfile.objects.get(user=user)
            context.update(csrf(request))
            return render(request,"editcard.html",context)
    else:
        context={'message': "no such blog available"}

    context.update(csrf(request))
    return render(request,"editcard.html",context)


@login_required(login_url="/users/login/")
def newcard(request):
    if request.method == 'POST':
        try:
            name=request.POST.get("name")
            image=request.FILES.get("image")
            desc =request.POST.get("desc")
            v_type=request.POST.get("type")
            user = request.user
            user=UserProfile.objects.get(user=user)

            blog=Cards(
                name=name,
                image=image,
                desc=desc,
                user=user)
            blog.save()
            context = {
                "status": True, 'message': "Profile Saved."
            }
            context.update(csrf(request))
            return render_to_response("allcards.html", context)
        except:
            context = {
                "status": False, 'message': "Profile Not Saved."
            }
            context.update(csrf(request))
            return render_to_response("newcard.html", context)
    else:
        context = {
                "status": "onhold", 'message': "Write a Blog!!"
            }
        context.update(csrf(request))
        return render_to_response("newcard.html", context)

def users_cards(request):
    context={}
    #import ipdb; ipdb.set_trace()
    if request.method == "GET":
        cards = Cards.objects.all()

        paginator = Paginator(cards, 30)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            cards = paginator.page(page)
        except(EmptyPage, InvalidPage):
            cards = paginator.page(paginator.num_pages)
        context = {
            'cards': cards

        }
    context.update(csrf(request))
    return render(request, "users_blogs.html", context)
