from django.shortcuts import render
from .models import Journal
from .forms import JournalForm
from Users.models import UserProfile
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from Blogs.models import Cards
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url="/users/login")
def create_journal(request):
	context = {}
	if request.method=="GET":
		form = JournalForm()
		context = {
			"form":form,
			"Message" :"Add Your Favorite Blogs to your journal here"
		}
		context.update(csrf(request))
		return render(request,"create_journal.html",context)
	else:
		user= request.user
		form = JournalForm(request.POST or None)
		user = UserProfile.objects.get(user=user)
		context={
			"form":form,
			'message': "enter details"
		}
		if form.is_valid():
			instance= form.save(commit=False)
			instance.user=user
			instance.save()
			context={"message":"journal created successfully"}
		else:
			context={"message":"something went wrong. please enter the details again."}
			context.update(csrf(request))
			return render(request,"create_journal.html",context)
	context.update(csrf(request))
	return HttpResponseRedirect("/cards/all/")

@login_required(login_url="/users/login")
def show_all(request,name):
	#import ipdb; ipdb.set_trace()
	context={}
	if  str(request.user)==name:
		user=name
		user=User.objects.get(username=user)
		user=UserProfile.objects.get(user=user)
		user_journal = Journal.objects.get(user=user)
		user_journal=user_journal.collection.all()
		context={
			"user":user,
			"user_journal": user_journal,
		}
		context.update(csrf(request))
		return render(request,"user_journal.html",context)



@login_required(login_url="/users/login")
def add_single(request,name):
	context={}
	#import ipdb; ipdb.set_trace()
	if request.method=="POST":
		user=request.user
		user = UserProfile.objects.get(user=user)
		user_journal = Journal.objects.get(user=user)
		card=Cards.objects.get(slug=name)
		if user.my_journal.filter(collection=card).exists():
			context = {
				"button_text": "delete"
			}
			user_journal.collection.remove(card)
		else:
			context={
				"button_text":"add"
			}
			user_journal.collection.add(card)
	return HttpResponseRedirect("/cards/all/%s/" % name, context)