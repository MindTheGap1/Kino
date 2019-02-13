from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from movies.models import Genres
from .forms import GenreSelect

def genrePick(request):
	template = 'genre_pick.html'
	if request.method == 'POST':
		form = GenreSelect(request.POST)
		if form.is_valid():
			genres = form.cleaned_data.get('pickedGenres')
			#Add rows to bridge table where userid = current user id and genreid(s) are equated to picked genres
			#need to find out how the cleaned data stores it - i.e. as plain text, genre objects or genre ids
			return redirect('/')
		
	genre_list = Genres.objects.order_by('genreName')
	context = {
		'genre_list': genre_list,
		'genre_form': GenreSelect,
	}
	return render(request, template, context)