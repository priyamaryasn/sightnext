"""Filter."""
from django import template
from FollowCategory.models import BlogsCategory
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
	list=[]
	cat_names=values.blog_in_cat.all()
	for value in cat_names:
		list.append(value)
	return list