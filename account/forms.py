from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from movies.models import Genre

class Register(UserCreationForm):
	email = forms.EmailField(required = True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(Register, self).save(commit = False)
		user.email = self.cleaned_data["email"]

		if commit:
			user.save()
		return user
class GenreSelect(forms.Form):
	genres = Genre.objects.all()
	options = [(genre.genreId, genre.genreName) for genre in genres]
	pickedGenres = forms.MultipleChoiceField(label='', widget=forms.CheckboxSelectMultiple, choices=options)