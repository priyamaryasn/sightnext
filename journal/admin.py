from django.contrib import admin
from .models import Journal
from .forms import JournalForm
# Register your models here.


admin.site.register(Journal)