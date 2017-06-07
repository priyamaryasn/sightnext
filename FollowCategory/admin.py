from django.contrib import admin
from .models import CategoryFollowers,BlogsCategory
# Register your models here.

class CategoryFollowersAdmin(admin.ModelAdmin):
	
	
	def all_cat(self, obj):
		return ", ".join([x.name for x in obj.cat.all()])
	
	list_display=["user","all_cat"]
	search_fields=["user","cat"]
	class Meta:
		model = CategoryFollowers




class BlogsCategoryAdmin(admin.ModelAdmin):
	
	list_display=['category','all_blogs']
	
	def all_blogs(self,obj):
		return ", ".join([x.name for x in obj.blogs.all()])
	
	class Meta:
		model = BlogsCategory

admin.site.register(CategoryFollowers,CategoryFollowersAdmin)
admin.site.register(BlogsCategory,BlogsCategoryAdmin)