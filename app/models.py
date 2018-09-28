from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Models for interest of a person
class Interest(models.Model):
	interest = models.CharField(max_length = 50, help_text='Add your interest')
	'''person = models.ForeignKey(Person, on_delete=models.CASCADE)'''

	def __str__ (self):
		return self.interest
'''
#Model for a person. Many to many field for an interest (A person can have multiple
interests and an interest can be of multiple person). One to one key for person (
For each instance of person there should be a user linked with it).
'''
class Person(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length = 50)
	bio = models.TextField()
	profilePic = models.ImageField(upload_to = '', default = 'no-img.jpg')
	interest = models.ManyToManyField(Interest, help_text='Select a interest for this person')

	def __str__(self):
		return self.name
