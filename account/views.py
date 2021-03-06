from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.management import call_command
from django.db.models import Q
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as Auth_User
from movies.models import Genre
from .models import FavouriteGenres, User, UserMovieStats
from .forms import GenreSelect


class signup(generic.CreateView):
	form_class = UserCreationForm
	success_url = '/login'
	template_name = 'account/signup.html'

	def form_valid(self, form):
		form.save()
		self.request.session['success_signup'] = True
		return redirect(self.success_url)

def profile(request):
	if not request.user.is_authenticated:
		return redirect('/landing/')
	else:
		user_id = request.user.id
		if User.objects.filter(user_id = user_id):
			if User.objects.get(user_id = user_id).completedTutorial == False:
				return redirect('/genre/')
		else:
			User.objects.create(user_id = user_id, completedTutorial = False)
			return redirect('/genre/')
		template = 'account/profile.html'
		return render(request, template)


def genrePick(request):
	if not request.user.is_authenticated:
		return redirect('/login/?next=/genre')
	else:
		user_id = request.user.id
		current_user_object = Auth_User.objects.get(id=user_id)
		try:
			user_entry = User.objects.get(user_id = user_id)
		except User.DoesNotExist:
			user_entry = User.objects.create(user_id = user_id, name = current_user_object.username, completedTutorial=False)
			user_entry.save()
		if request.method == 'POST':
			form = GenreSelect(request.POST)
			if form.is_valid():
				FavouriteGenres.objects.filter(userId = current_user_object).delete()
				genres = form.cleaned_data.get('pickedGenres')

				for genre in genres:
					genreObject = Genre.objects.get(genreId=genre)
					FavouriteGenres.objects.create(userId = current_user_object,
													genreId = genreObject)

				ratings = UserMovieStats.objects.filter(Q(userId = current_user_object), ~Q(rating=None))
				if ratings:
					call_command('getrecommends', user_id=[user_id])
				else:
					call_command('getcoldstart', user_id=[user_id])
				#Tell DB that this user has done the cold-start
				if User.objects.filter(user_id = current_user_object):
					User.objects.filter(user_id = current_user_object).update(completedTutorial=True)
				else:
					User.objects.create(user = current_user_object, completedTutorial=True)

				return redirect('/')


		genreIds = Genre.objects.all().values_list('genreId', flat=True)
		genreQ = FavouriteGenres.objects.filter(userId=current_user_object)
		preselect = []
		for genre in genreQ:
			preselect += [genre.genreId.genreId]
		template = 'account/genre_pick.html'
		form = GenreSelect(initial={'pickedGenres': preselect})
		context = {
			'genre_ids': genreIds,
			'genre_form': form
		}
		return render(request, template, context)
