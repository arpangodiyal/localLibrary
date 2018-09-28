from django.urls import path

from . import views

urlpatterns = [
	path('register',views.register, name='register'),
	path('login', views.login, name='login'),
    path('', views.index, name='index'),
    path('<int:person_id>/', views.showDetails, name='showDetails'),
    path('getDetails', views.getDetails, name='getDetails'),
    path('logout', views.logoutView, name='logoutView'),
    path('edit/<int:person_id>/', views.editDetails, name='editDetails'),
    path('delete/<int:person_id>/', views.deletePerson, name='deletePerson'),
]