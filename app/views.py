from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Person, Interest
from .forms import PersonForm, LoginForm, SearchForm

# Create your views here.

#View to register a user. Using the inbuilt user creation form.
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request, "home.html")
		return render(request, 'register.html', {'form' : form})
	else:
		form = UserCreationForm()
		return render(request, "register.html", {'form' : form})

#Login view
def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			auth_login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			return render(request, 'login.html', {'form' : form})
	else:
		form = LoginForm()
		return render(request, "login.html", {'form' : form})

#The decorator avoids a not registered user from accessing the submit details page.
@login_required
def getDetails(request):
	if request.method == 'POST':
		user = request.user

		if request.FILES:
			form = PersonForm(request.POST,request.FILES)

		else:
			form = PersonForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			bio = form.cleaned_data['bio']
			profilePic = form.cleaned_data['profilePic']
			b = Person(name=name, bio=bio, profilePic=profilePic, user=user)
			b.save()

			for i in form.cleaned_data['interest']:
				b.interest.add(i)

			return render(request, "index.html", {'persons':Person.objects.all()})
		else:
			return render(request, 'getDetails.html', {'form' : form})
		
	else:
		form = PersonForm()
		return render(request, 'getDetails.html', {'form' : form})

#It is a view which shows all the registered users who have entered their details
# f is used to check whether a user has submitted his details or not. If not enter
# details link is given. Else edit your details link is given.Edit your details link is
# given in front of the logged in user.
def index(request):
	user = request.user
	form = SearchForm()
	persons = Person.objects.all()
	f = 0
	for p in persons:
		if p.user == user:
			f = 1
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			persons = Person.objects.all().filter(name__startswith=name)
			return render(request, 'index.html', {'persons' : persons, 'user' : user, 
			'f' : f, 'form' : form})

	else:
		return render(request, 'index.html', {'persons' : persons, 'user' : user, 
			'f' : f, 'form' : form})

#View to show the details of the person with the given ID as passed by the URL.
def showDetails(request, person_id):
	person = get_object_or_404(Person, pk=person_id)
	interests = person.interest.all()
	return render(request, "showDetails.html", {'person' : person, 'interests' : interests})

#Logout view.
def logoutView(request):
	logout(request)
	return HttpResponseRedirect('/')

#This view updates the information about the person as sepicified by the person id
#given in the url. It checks whether a person is logged in or not before making 
#changes.
def editDetails(request, person_id):
	person = get_object_or_404(Person, pk=person_id)
	user = request.user
	if person.user != user:
		return HttpResponse('You are not allowed to access this page.')
	else:
		if request.method == 'POST':

			if request.FILES:
				form = PersonForm(request.POST,request.FILES)
			else:
				form = PersonForm(request.POST)

			if form.is_valid():
				person.name = form.cleaned_data['name']
				person.bio = form.cleaned_data['bio']
				person.profilePic = form.cleaned_data['profilePic']
				person.save()

				for p in person.interest.all():
					person.interest.remove(p)

				for p in form.cleaned_data['interest']:
					person.interest.add(p)
				return HttpResponseRedirect(reverse('index'))

		else:
			data = {'name' : person.name, 'bio' : person.bio, 'interest' : 
			person.interest.all()}
			form = PersonForm(initial=data)
			return render(request, 'getDetails.html', {'form' : form})

'''
A view which deletes a person as specified by the url. A person should be logged in
to delete his/her instance.
'''
def deletePerson(request, person_id):
	person = get_object_or_404(Person, pk=person_id)
	user = request.user
	if person.user != user:
		return HttpResponse('You are not allowed to access this page.')
	else:
		person.delete()
		request.user.delete()
		return HttpResponseRedirect(reverse('index'))
		
