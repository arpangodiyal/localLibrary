from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from app.models import Person, Interest

class PersonForm(ModelForm):
	class Meta:
		model = Person
		fields = ['name', 'bio','interest', 'profilePic']

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30, help_text='Enter your Username', required=True)
	password = forms.CharField(widget=forms.PasswordInput, help_text='Password', required=True)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user:
			raise forms.ValidationError("Sorry, that login was invalid. Please try again.")

class SearchForm(forms.Form):
	name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Search'}))

