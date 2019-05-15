from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class ContactPerson(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=35)
	last_name = models.CharField(max_length=35)
	contact_number = PhoneNumberField(unique=True)
	address = models.TextField()

	def __str__(self):
		return self.first_name + " " + self.last_name




