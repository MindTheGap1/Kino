from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from search.forms import SearchBar

from .models import *

def index(request):
    movie_list = Movies.objects.order_by('overallRating')
    genre_list = Genres.objects.order_by('genreName')
    search_form = SearchBar

    template = 'movies/index.html'
    context = {
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)

def detail(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    link = movie.trailerLink
    pos = link.find('?v=')
    vidId = link[pos + 3: len(link)]
    directors = []
    writers = []
    actors = []
    genres = []

    directorsQ = MovieDirectors.objects.filter(movieId=movie_id)
    directors = Directors.objects.filter(movies__in=directorsQ)

    writersQ = MovieWriters.objects.filter(movieId=movie_id)
    writers = Writers.objects.filter(movies__in=writersQ)

    actorsQ = MovieActors.objects.filter(movieId=movie_id)
    actors = Actors.objects.filter(movies__in=actorsQ)

    genreQ = MovieGenres.objects.filter(movieId=movie_id)
    genres = Genres.objects.filter(movies__in=genreQ)

    template = 'movies/detail.html'
    context = {
        'movie': movie,
        'vidId': vidId,
        'writers': writers,
        'directors': directors,
        'actors': actors,
        'genres': genres,
    }
    return render(request, template, context)


def genre_detail(request, genre_id):
    selected_genre = get_object_or_404(Genres, pk=genre_id)

    moviesQ = MovieGenres.objects.filter(genreId=genre_id)
    movie_list = Movies.objects.filter(genres__in=moviesQ).order_by('overallRating')

    genre_list = Genres.objects.order_by('genreName')
    search_form = SearchBar

    template = 'movies/genre_detail.html'
    context = {
        'selected_genre': selected_genre,
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)

def actor_detail(request, actor_id):
    selected_actor = get_object_or_404(Actors, pk=actor_id)

    moviesQ = MovieActors.objects.filter(actorId=actor_id)
    movie_list = Movies.objects.filter(actors__in=moviesQ).order_by('overallRating')
    
    genre_list = Genres.objects.order_by('genreName')
    search_form = SearchBar

    template = 'movies/actor_detail.html'
    context = {
        'selected_actor': selected_actor,
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)

def director_detail(request, director_id):
    selected_director = get_object_or_404(Directors, pk=director_id)

    moviesQ = MovieDirectors.objects.filter(directorId=director_id)
    movie_list = Movies.objects.filter(directors__in=moviesQ).order_by('overallRating')
    
    genre_list = Genres.objects.order_by('genreName')
    search_form = SearchBar

    template = 'movies/genre_detail.html'
    context = {
        'selected_director': selected_director,
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)

def writer_detail(request, writer_id):
    selected_writer = get_object_or_404(Writers, pk=writer_id)

    moviesQ = MovieWriters.objects.filter(writerId=writer_id)
    movie_list = Movies.objects.filter(writers__in=moviesQ).order_by('overallRating')
    
    genre_list = Genres.objects.order_by('genreName')
    search_form = SearchBar

    template = 'movies/writer_detail.html'
    context = {
        'selected_writer': selected_writer,
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)