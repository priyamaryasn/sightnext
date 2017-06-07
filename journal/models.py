from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from Users.models import UserProfile
from Blogs.models import Cards
# Create your models here.
class Journal(models.Model):
	user = models.ForeignKey(UserProfile, related_name='my_journal')
	title = models.CharField(max_length=255, default="anonymous",blank=False)
	collection = models.ManyToManyField(Cards, related_name='cards')

	def __str__(self):
		return str(self.user)

	class Meta:
		verbose_name_plural = "MyJournals"
		verbose_name = "MyJournals"