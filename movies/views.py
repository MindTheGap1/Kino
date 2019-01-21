from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import Movies, Genres

def index(request):
    movie_list = Movies.objects.order_by('overallRating')
    genre_list = Genres.objects.order_by('genreName')
    template = 'movies/index.html'
    context = {
        'movie_list': movie_list,
        'genre_list': genre_list
    }
    return render(request, template, context)

def detail(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})