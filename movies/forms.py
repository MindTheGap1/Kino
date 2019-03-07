from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from movies.models import Genre

class Rate(forms.Form):
	RATINGS=[('1','1'),('2','2'),('3','3'),('4','4')]

	rating = forms.ChoiceField(choices=RATINGS, widget=forms.RadioSelect)