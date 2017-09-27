"""Filter."""
from django import template
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from Users.models import UserProfile
from FollowCategory.models import BlogsCategory
from Blogs.models import Cards
register = template.Library()


@register.filter
def filter_private_cards(values):
    # import ipdb; ipdb.set_trace()
    all_list = []
    for value in values:
        if (value.v_type == 'private'):
            all_list.append(value)

    return all_list

@register.filter
def cards_category(values):
	#import ipdb; ipdb.set_trace()
	all_list=[]
	cat_names=values.blog_in_cat.all()
	for value in cat_names:
		all_list.append(value)
	return all_list

@register.filter
def card_likes(user,name):
	
	import ipdb; ipdb.set_trace()
	card = get_object_or_404(Cards,name=name)
	user = UserProfile.objects.get(name=user)
	return (card.card_likes.filter(user=user).exists())
	
