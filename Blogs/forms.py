from django import forms
from .models import Cards

from froala_editor.widgets import FroalaEditor

class CardsForm(forms.ModelForm):
	
	desc = forms.CharField(widget=FroalaEditor)
	

	class Meta:
		model = Cards
		fields = ['name', 'image', 'desc', 'v_type']
