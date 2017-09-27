from django import forms
from .models import Cards
from django.utils.text import slugify
import random
import string
import itertools


from froala_editor.widgets import FroalaEditor

class CardsForm(forms.ModelForm):
	
	desc = forms.CharField(widget=FroalaEditor)
	

	class Meta:
		model = Cards
		fields = ['name','desc', 'v_type','blog_category']

	def save(self,user):
		instance = super(CardsForm, self).save(commit=False)

		max_length = Cards._meta.get_field('slug').max_length
		instance.slug = orig = slugify(instance.name)[:max_length]
		
		instance.user=user

		for x in itertools.count(1):
		    if not Cards.objects.filter(slug=instance.slug).exists():
		        break

		    # Truncate the original slug dynamically. Minus 1 for the hyphen.
		    extra = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(9))
		    instance.slug = "%s-%s" % (orig[:max_length - len(str(x)) - 1], extra)

		instance.save()

		return instance