from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from movies.models import Genre

class GenreSelect(forms.Form):
	genres = Genre.objects.all()
	options = [(genre.genreId, genre.genreName) for genre in genres]
	pickedGenres = forms.MultipleChoiceField(label='', widget=forms.CheckboxSelectMultiple, choices=options)