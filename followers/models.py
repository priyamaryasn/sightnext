from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from Users.models import UserProfile
#from categories.models import Categories
from django.utils import timezone
# Create your models here.

class Followers(models.Model):
	user = models.ForeignKey(UserProfile,related_name = "follower")
	follows = models.ManyToManyField(UserProfile,related_name="follow")
	followed_by = models.ManyToManyField(UserProfile, related_name="followed_bys")
	following_since = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.user)

	class Meta():
		verbose_name_plural = "Followers"
		verbose_name = "Followers"

"""class CategoryFollowers(models.Model):
	user = models.ForeignKey(UserProfile,related_name = "cat_follower")
	cat = models.ManyToManyField(Categories,related_name="cat_followed")
	
	def __str__(self):
		return str(user)

	class Meta:
		verbose_name = "User Folllowing Categories"
		verbose_name_plural = "User Folllowing Categories"
		"""