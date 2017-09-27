from django.shortcuts import render,get_object_or_404
from django.template.context_processors import csrf
from .models import Categories
from FollowCategory.models import BlogsCategory,CategoryFollowers
from Users.models import UserProfile

# Create your views here.
def all_cat(request):
	context={}
	if request.method == "GET":
		if str(request.user) != "AnonymousUser":
			user=request.user
			user=UserProfile.objects.get(user=user)
			user=CategoryFollowers.objects.get(user=user)
			all_cat=user.cat.all()
			cats=Categories.objects.all()
			context={"cats": cats,"user":user,"all_cat":all_cat}
		else:
			cats=Categories.objects.all()
			context={"cats": cats}
	context.update(csrf(request))
	return render(request,"all_category.html",context)

def all_blogs(request,name):
	#import ipdb; ipdb.set_trace()
	context={}
	instance = get_object_or_404(Categories,name=name)
	blog_list = BlogsCategory.objects.get(category=instance)
	blog_list = blog_list.blogs.all()
	context={
		'list':blog_list,
	}
	context.update(csrf(request))
	return render(request,"category_blogs.html",context)
