from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from movies.models import Genres

class GenreSelect(forms.Form):
	genres = Genres.objects.all()
	options = ()
	for genre in genres:
		options = options + ((genre.genreId, genre.genreName, ), )
	pickedGenres = forms.MultipleChoiceField(label='Pick your favourite genres:', widget=forms.CheckboxSelectMultiple, choices=options)