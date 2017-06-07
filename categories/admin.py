from django.contrib import admin
from .models import Categories
# Register your models here.

class catAdmin(admin.ModelAdmin):
	search_fields=["name"]
	class Meta:
		model=Categories

admin.site.register(Categories,catAdmin)
