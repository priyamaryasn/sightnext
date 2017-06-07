from django.contrib import admin
from .models import Cards
from .forms import CardsForm
# Register your models here.


class CardsAdmin(admin.ModelAdmin):
	form = CardsForm
	list_display = ['__str__', 'user',"upload_date"]
	list_display_links = ['user',"upload_date",'__str__']
	search_fields = ['name',"desc"]
	class Meta:
		model = Cards

admin.site.register(Cards, CardsAdmin)
