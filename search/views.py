from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from movies.models import Movies, Genres, MovieGenres, MovieWriters, MovieDirectors, MovieActors
from django.db.models import Q
from .forms import SearchBar

def searchMovie(request):
		phrase = request.POST.get("phrase", "")
		phrase = phrase.strip()

		actor_list = MovieActors.objects.filter(Q(actorId__actorFirstName__icontains=phrase) | Q(actorId__actorLastName__icontains=phrase))
		writer_list = MovieWriters.objects.filter(Q(writerId__writerFirstName__icontains=phrase) | Q(writerId__writerLastName__icontains=phrase))
		director_list = MovieDirectors.objects.filter(Q(directorId__directorFirstName__icontains=phrase) | Q(directorId__directorLastName__icontains=phrase))
		genre_list = MovieGenres.objects.filter(Q(genreId__genreName__icontains=phrase))

		movie_list = Movies.objects.filter(Q(movieName__icontains=phrase) | Q(description__icontains=phrase)
											| Q(genres__in=genre_list) 
											| Q(directors__in=director_list)
											| Q(writers__in=writer_list) 
											| Q(actors__in=actor_list)).order_by('overallRating').distinct() 
		total_genre_list = Genres.objects.order_by('genreName')



		search_form = SearchBar

		template = 'search/details.html'
		context = {
			'movie_list': movie_list,
			'total_genre_list': total_genre_list,
        	'search_form': search_form,
			'phrase': phrase,
			}
		return render(request, template, context)