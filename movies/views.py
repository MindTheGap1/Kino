from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import Movies

def index(request):
    movie_list = Movies.objects.order_by('-movieName')
    template = 'movies/index.html'
    context = {
        'movie_list': movie_list
    }
    return render(request, template, context)

def detail(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})