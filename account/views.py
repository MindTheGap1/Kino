from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as Auth_User
from movies.models import Genre
from .models import FavouriteGenres, User
from .forms import GenreSelect


class signup(generic.CreateView):
	form_class = UserCreationForm
	success_url = '/account/genre'
	template_name = 'signup.html'

def profile(request):
	if not request.user.is_authenticated:
		return redirect('/landing/')
	else:
		template = 'profile.html'
		return render(request, template)

def genrePick(request):
	if not request.user.is_authenticated:
		return redirect('/login/?next=/account/genre')
	if request.user.is_authenticated:
		user_id = request.user.id
		current_user_object = Auth_User.objects.get(id=user_id)
		if request.method == 'POST':
			form = GenreSelect(request.POST)
			if form.is_valid():
				FavouriteGenres.objects.filter(userId = current_user_object).delete()
				genres = form.cleaned_data.get('pickedGenres')
				for genre in genres:
					genreObject = Genre.objects.get(genreId=genre)
					FavouriteGenres.objects.create(userId = current_user_object,
													genreId = genreObject)

				return redirect('/')

		genreQ = FavouriteGenres.objects.filter(userId=current_user_object)
		preselect = []
		for genre in genreQ:
			preselect += [genre.genreId.genreId]
		template = 'account/genre_pick.html'
		form = GenreSelect(initial={'pickedGenres': preselect})
		context = {
			'genre_form': form,
		}
		return render(request, template, context)
	else:
		return redirect('/')
