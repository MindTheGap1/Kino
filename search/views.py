from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from movies.models import Movie, Genre
from django.db.models import Q
from functools import reduce
import operator
from .forms import SearchForm

def searchMovie(request):
		phrase = request.POST.get("phrase") if request.POST.get("phrase") != "" else "" #Stops it displaying "None"
		genre_select = request.POST.get("genre_select")
		sort_select = int(request.POST.get("sort_select")) if request.POST.get("sort_select") != None else 0
		movie_list, new_movie_list = [], []
		sorting_list = ['movieName', '-movieName', 'price', '-price', 'overallRating', '-overallRating', 'length', '-length', 'releaseDate', '-releaseDate']


		if phrase:
			phrase = phrase.strip()
			phrase_sep = phrase.split(" ")

			
			movie_list += Movie.objects.filter(		  reduce(operator.or_, (Q(movieName__icontains=word) for word in phrase_sep))
													| reduce(operator.or_, (Q(description__icontains=word) for word in phrase_sep))
													| reduce(operator.or_, (Q(actors__actorFirstName__icontains=word) for word in phrase_sep))
													| reduce(operator.or_, (Q(actors__actorLastName__icontains=word) for word in phrase_sep))
													| reduce(operator.or_, (Q(writers__writerFirstName__icontains=word) for word in phrase_sep))
													| reduce(operator.or_, (Q(writers__writerLastName__icontains=word) for word in phrase_sep))
													| reduce(operator.or_, (Q(directors__directorFirstName__icontains=word) for word in phrase_sep))
													| reduce(operator.or_, (Q(directors__directorLastName__icontains=word) for word in phrase_sep))
													| reduce(operator.or_, (Q(genres__genreName__icontains=word) for word in phrase_sep))).distinct().order_by(sorting_list[sort_select])
		else:
			movie_list = Movie.objects.order_by('movieName').order_by(sorting_list[sort_select])


		if genre_select:
			for movie in movie_list:
				movie_genres = list(movie.genres.all().values_list('genreId', flat=True))
				new_movie_list.append(movie) if int(genre_select) in movie_genres else None
			movie_list = new_movie_list

		total_genre_list = Genre.objects.order_by('genreName')
		search_form = SearchForm(initial={'genre_select': genre_select, 
											'phrase': phrase,
											'sort_select': sort_select,})

		template = 'search/details.html'
		context = {
			'movie_list': movie_list,
			'total_genre_list': total_genre_list,
        	'search_form': search_form,
			'phrase': phrase,
			}
		return render(request, template, context)