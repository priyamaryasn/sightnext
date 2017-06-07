from __future__ import unicode_literals

from django.db import models
from Blogs.models import Cards
from Users.models import UserProfile
from categories.models import Categories
# Create your models here.

class CategoryFollowers(models.Model):
	user = models.OneToOneField(UserProfile,related_name = "cat_follower")
	cat = models.ManyToManyField(Categories,related_name="cat_followed",blank=True)
	
	def __str__(self):
		return str(self.user)

	class Meta:
		verbose_name = "User Folllowing Categories"
		verbose_name_plural = "User Folllowing Categories"

class BlogsCategory(models.Model):
	category = models.OneToOneField(Categories,related_name="cat_name")
	blogs = models.ManyToManyField(Cards, related_name="blog_in_cat",blank=True)

	def __str__(self):
		return str(self.category)


	class Meta:
		verbose_name = "Blogs in Categories"
		verbose_name_plural = "Blogs in Categories"