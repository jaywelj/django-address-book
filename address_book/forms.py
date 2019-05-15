from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import ContactPerson


class RegisterForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name",
		          "password1", "password2",)

class ContactPersonForm(forms.ModelForm):

	class Meta:
		model = ContactPerson
		fields = ("first_name", "last_name", "contact_number", "address")
		