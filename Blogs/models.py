from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from Users.models import UserProfile
from django.contrib.auth.models import User
from categories.models import Categories
from django.core.urlresolvers import reverse
from froala_editor.fields import FroalaField
# Create your models here.

TYPE_CHOICES = (("public", "public"), ("private", "private"))


class Cards(models.Model):
    """Creating a model."""

    user = models.ForeignKey(
        UserProfile,
        default="",
        null=True,
        blank=True)

    slug = models.SlugField(unique=True,default="nothing")

    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,verbose_name="Title")

    image = models.ImageField(
        upload_to='Cards',
        blank=True,
        null=True,
        verbose_name="Banner Image for your blog")

    desc = FroalaField(null=True,blank=True)

    v_type = models.CharField(max_length=125, choices=TYPE_CHOICES, default="public")

    blog_category = models.ManyToManyField(Categories,blank=True,related_name="category")

    likes = models.IntegerField(default=0)
    

  

    upload_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Uploaded On")

    def __str__(self):
        """Show on admin."""
        return self.name
    
    def get_absolute_url(self):
        return reverse("cards:view_card",kwargs={"name": self.slug})
    class Meta:
        """This will show on admin main page."""

        verbose_name = 'Blogs'
        verbose_name_plural = "Blogs"


  # liked_by = models.ForeignKey(
    #     User,
    #     default="",
    #     related_name='likedby',
    #     null=True,
    #     blank=True)

