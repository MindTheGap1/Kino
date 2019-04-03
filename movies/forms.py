<<<<<<< HEAD
from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from movies.models import Genre

class Rate(forms.Form):
	RATINGS=[('1','1'),('2','2'),('3','3'),('4','4')]

	rating = forms.ChoiceField(choices=RATINGS, widget=forms.RadioSelect)
=======
from django import forms
from account import models

class RatingForm(forms.ModelForm):
    ratings_choice = [
        ("1","Didn't like it at all"),
        ("2","It wasn't great"),
        ("3","It's ok"),
        ("4","It was good"),
        ("5","I loved it"),
    ]
    rating = forms.ChoiceField(label = "", choices = ratings_choice, widget=forms.RadioSelect(attrs={'class' : 'ratingbutton'}))

    class Meta:
        model = models.UserMovieStats
        fields = ('rating',)
>>>>>>> 2105ebee5a4802987251f72383949e7a6d54b5b6
