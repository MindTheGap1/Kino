from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from search.forms import SearchForm
from movies.forms import RatingForm
from account.models import UserMovieStats
from django.contrib import auth
from django.contrib.auth.models import User

from .models import *

def index(request):
    movie_list = Movie.objects.order_by('overallRating')
    genre_list = Genre.objects.order_by('genreName')
    search_form = SearchForm

    template = 'movies/index.html'
    context = {
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    link = movie.trailerLink
    pos = link.find('?v=')
    vidId = link[pos + 3: len(link)]
    form = RatingForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        #IMPORTANT: for some reason my own copy of the database IDs users in auth_users starting from 8 whereas
        # it IDs users in Users starting from 1, this means that it is not able to find foreign keys unless you subtract 7
        # this needs to be fixed 
        post.userId_id = request.user.id - 7
        post.movieId_id = movie_id
        post.save()
        rating = form.cleaned_data['rating']

    #form.save()
    
    template = 'movies/detail.html'
    context = {
        'movie': movie,
        'vidId': vidId,
        'form': form
    }
    return render(request, template, context)


def genre_detail(request, genre_id):
    selected_genre = get_object_or_404(Genre, pk=genre_id)

    movie_list = Movie.objects.filter(genres__genreId=genre_id).order_by('overallRating')

    genre_list = Genre.objects.order_by('genreName')
    search_form = SearchForm

    template = 'movies/genre_detail.html'
    context = {
        'selected_genre': selected_genre,
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)

def actor_detail(request, actor_id):
    selected_actor = get_object_or_404(Actor, pk=actor_id)

    movie_list = Movie.objects.filter(actors__actorId=actor_id).order_by('overallRating')
    
    genre_list = Genre.objects.order_by('genreName')
    search_form = SearchForm

    template = 'movies/actor_detail.html'
    context = {
        'selected_actor': selected_actor,
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)

def director_detail(request, director_id):
    selected_director = get_object_or_404(Director, pk=director_id)

    movie_list = Movie.objects.filter(directors__directorId=director_id).order_by('overallRating')
    
    genre_list = Genre.objects.order_by('genreName')
    search_form = SearchForm

    template = 'movies/genre_detail.html'
    context = {
        'selected_director': selected_director,
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)

def writer_detail(request, writer_id):
    selected_writer = get_object_or_404(Writer, pk=writer_id)

    movie_list = Movie.objects.filter(writers__writerId=writer_id).order_by('overallRating')
    
    genre_list = Genre.objects.order_by('genreName')
    search_form = SearchForm

    template = 'movies/writer_detail.html'
    context = {
        'selected_writer': selected_writer,
        'movie_list': movie_list,
        'genre_list': genre_list,
        'search_form': search_form,
    }
    return render(request, template, context)
