from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q, Count
from search.forms import SearchForm
from datetime import datetime, timedelta

from .models import *

def index(request):
    twoDaysAgo = datetime.now() - timedelta(days=2)
    movie_list = Movie.objects.order_by('overallRating').annotate(
                            isUnwatched=Count('order', filter=Q(order__movieStartTime = None)),
                            startedWatching=Count('order', filter=Q(order__movieStartTime__gte = twoDaysAgo )))
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

    template = 'movies/detail.html'
    context = {
        'movie': movie,
        'vidId': vidId,
    }
    return render(request, template, context)


def genre_detail(request, genre_id):
    twoDaysAgo = datetime.now() - timedelta(days=2)
    selected_genre = get_object_or_404(Genre, pk=genre_id)

    movie_list = Movie.objects.filter(genres__genreId=genre_id).order_by('overallRating').annotate(
                            isUnwatched=Count('order', filter=Q(order__movieStartTime = None)),
                            startedWatching=Count('order', filter=Q(order__movieStartTime__gte = twoDaysAgo )))

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
    twoDaysAgo = datetime.now() - timedelta(days=2)
    selected_actor = get_object_or_404(Actor, pk=actor_id)

    movie_list = Movie.objects.filter(actors__actorId=actor_id).order_by('overallRating').annotate(
                            isUnwatched=Count('order', filter=Q(order__movieStartTime = None)),
                            startedWatching=Count('order', filter=Q(order__movieStartTime__gte = twoDaysAgo )))
    
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
    twoDaysAgo = datetime.now() - timedelta(days=2)
    selected_director = get_object_or_404(Director, pk=director_id)

    movie_list = Movie.objects.filter(directors__directorId=director_id).order_by('overallRating').annotate(
                            isUnwatched=Count('order', filter=Q(order__movieStartTime = None)),
                            startedWatching=Count('order', filter=Q(order__movieStartTime__gte = twoDaysAgo )))
    
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
    twoDaysAgo = datetime.now() - timedelta(days=2)
    selected_writer = get_object_or_404(Writer, pk=writer_id)

    movie_list = Movie.objects.filter(writers__writerId=writer_id).order_by('overallRating').annotate(
                            isUnwatched=Count('order', filter=Q(order__movieStartTime = None)),
                            startedWatching=Count('order', filter=Q(order__movieStartTime__gte = twoDaysAgo )))
    
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
