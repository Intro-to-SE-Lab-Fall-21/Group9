from typing import Optional
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=False)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ComposeMessage(forms.Form):
	subject = forms.CharField(label='Subject')
	message = forms.CharField(label='Message')
	recipient = forms.EmailField(label='Recipient')
	#file = forms.FileField(label='Attatchment')
	file = forms.FileField(required=False, label='Attatchment')
