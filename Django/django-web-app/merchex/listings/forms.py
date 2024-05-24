from django import forms
from listings.models import Band, Ad

class ContactUsForm(forms.Form):
	nom = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField(max_length=1000)

class BandForm(forms.ModelForm):
	class Meta:
		model =Band
		exclude = ('active', 'official_homepage')

class AdForm(forms.ModelForm):
	class Meta :
		model = Ad
		fields = '__all__'