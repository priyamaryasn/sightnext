from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from categories.models import Categories
from Users.models import UserProfile
from .models import CategoryFollowers
from django.template.context_processors import csrf
# Create your views here.
def checko(request):
	return render(request,"checko.html",{})

def follow_cat(request,name):
	#import ipdb; ipdb.set_trace()
	context={}
	if request.method=="POST":
		cat= get_object_or_404(Categories,name=name)
		user=request.user
		user=UserProfile.objects.get(user=user)
		cat_user= CategoryFollowers.objects.get(user=user)
		if CategoryFollowers.objects.filter(user=user,cat=cat).exists():
			cat_user.cat.remove(cat)
			message="unsubscribed"
		else:
			cat_user.cat.add(cat)
			message="subscribed"
		context={
			"message":message,
			"user":user
		}
	context.update(csrf(request))
	return HttpResponseRedirect("/categories/")

