from django import forms

from .models import *

class CertiForm(forms.ModelForm):

	class Meta:
		model = Certificate
		fields = "__all__"