from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from categories.models import Categories
from Users.models import UserProfile
from .models import CategoryFollowers,BlogsCategory
from django.template.context_processors import csrf
# Create your views here.
def checko(request):
	import ipdb; ipdb.set_trace()
	li = ["Startups","Technology","People","Politics","News","Business","Marketing","Development","Photography","Movies","Education","Travel","Venture Capital","Sports","Food","Social" "Media","Software","Poetry","Bots","Fiction","Government","Video" "Games","Nature","News-Satire","Advertising","Virtual",'Reality',"Artifiacial Intelligence","Engineering","Entrepreneurship","Internet of Things","Science","Books",'Health',"Visiting and Travel","Music","Creativity","Psychology","Design","History","Economics","Cooking","Entertainment","Writing",'Literature',"Finance","Fashion and Style","Mathematics","Ideas","Sarcasm","TV","Novels","Dating and Relationships","Inspiration","Medicines and Healthcare","Journalism",'Philosophy',"Physics","Investment",'Nutrition',"Writer and Authors","Small" "Businesses","Art & Culture",'Architecture',"Space","Feminism","Leadership","Women","Humans"]
	for item in li:
		cat=Categories(name=item)
		cat.save()
		print ("done")
	categories=Categories.objects.all()
	for item in categories:
	    cat=BlogsCategory(category=item)
	    cat.save()
	    print("alsodone")
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

