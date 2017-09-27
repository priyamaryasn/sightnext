from django.contrib import admin
from .models import Categories
# Register your models here.

class catAdmin(admin.ModelAdmin):
	search_fields=["name"]
	list_display=["__str__","blog_count","user_count"]
	class Meta:
		model=Categories

admin.site.register(Categories,catAdmin)
