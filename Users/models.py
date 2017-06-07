from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

GENDER_CHOICES = (('Others', 'Others'), ("Male", "Male"), ("Female", "Female"))


class UserProfile(models.Model):

    user = models.OneToOneField(User, verbose_name="related to")

    name = models.CharField(max_length=200, null=False, blank=False)

    email = models.EmailField(null=False, blank=False)
    

    joining_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = " Users"


class UserProfileInfo(models.Model):

    userlink = models.OneToOneField(UserProfile, verbose_name="of user",related_name="user_info")

    full_name = models.CharField(max_length=255, null=True, blank=True)

    gender = models.CharField(max_length=125, choices=GENDER_CHOICES)

    profile_pic = models.ImageField(upload_to="users", null=True, blank=True,verbose_name="Add a Profile Pic" ,default="user_default.png")
    about = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name = "UsersInfo"
        verbose_name_plural = "UsersInfo"

    def __str__(self):
        return str(self.userlink)
