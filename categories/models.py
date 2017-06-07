from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
class Categories(models.Model):
	name = models.CharField(max_length = 25,blank=False, null=False,default="None",unique=True)
	image = models.ImageField(
        		upload_to='Categories',
        		blank=False,
        		null=False,
        		verbose_name="Category Image",
        		default='no-image.png')
	user_count = models.IntegerField(default=0)
	blog_count = models.IntegerField(default=0)
	

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse("category:all_blogs",kwargs={'name':self.name})
	class Meta:
		verbose_name_plural = "Categories"
		verbose_name = "Categories"