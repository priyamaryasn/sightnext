from django import template
register = template.Library()

@register.filter
def filter_users_cards(values):
	all_list = []
	username = card.user.username
	for value in values:
		if (value.user == username):
			all_list.append(values)
	return all_list