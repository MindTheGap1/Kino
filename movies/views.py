from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Exists, OuterRef, Subquery
from search.forms import SearchForm
from movies.forms import RatingForm
from cart.forms import CartAddProductForm
from account.models import UserMovieStats
from django.contrib.auth.models import User as Auth_User
from datetime import datetime, timedelta

from .models import *
from orders.models import OrderItem

def index(request):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now() - timedelta(days=2)
        ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
                                                    movieId__movieId = OuterRef('pk'),
                                                    movieStartTime = None).values('movieStartTime')
        ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
                                                    movieId__movieId = OuterRef('pk'), 
                                                    movieStartTime__gte = twoDaysAgo).values('movieStartTime')
        recValue = UserMovieStats.objects.filter(userId = current_user_object,
                                                movieId__movieId = OuterRef('pk')).values('recommendValue')
        movie_list = Movie.objects.annotate(
                                recValue=Subquery(recValue),
                                isUnwatched=Exists(ordersUnwatched),
                                startedWatching=Exists(ordersStarted)).order_by(
                                '-recValue')
        

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
    current_user_object = Auth_User.objects.get(pk=request.user.id)
    link = movie.trailerLink
    pos = link.find('?v=')
    vidId = link[pos + 3: len(link)]
    form = RatingForm(request.POST)
    #test=a()
    match = UserMovieStats.objects.filter(userId=current_user_object, movieId = movie)
    if form.is_valid():
        if not match:
            #User is rating for first time
            post = form.save(commit=False)
            post.userId = current_user_object
            post.movieId = movie
            post.save()
        else:
            match[0].userId = current_user_object
            match[0].movieId = movie
            match[0].rating = form.cleaned_data['rating']
            match[0].save()

    if match[0].rating:
        filmrating = int(match[0].rating)
    else:
        filmrating = 0

    cart_form = CartAddProductForm()
    template = 'movies/detail.html'
    context = {
        'movie': movie,
        'vidId': vidId,
        'form': form,
        'cart_form': cart_form,
        'rating': filmrating,
    }
    return render(request, template, context)


def genre_detail(request, genre_id):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now() - timedelta(days=2)
        selected_genre = get_object_or_404(Genre, pk=genre_id)
        ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
                                                    movieId__movieId = OuterRef('pk'),
                                                    movieStartTime = None).values('movieStartTime')
        ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
                                                    movieId__movieId = OuterRef('pk'), 
                                                    movieStartTime__gte = twoDaysAgo).values('movieStartTime')
        recValue = UserMovieStats.objects.filter(userId = current_user_object,
                                                movieId__movieId = OuterRef('pk')).values('recommendValue')
        movie_list = Movie.objects.filter(genres__genreId=genre_id).order_by('overallRating').annotate(
                                recValue=Subquery(recValue),
                                isUnwatched=Exists(ordersUnwatched),
                                startedWatching=Exists(ordersStarted)).order_by(
                                '-recValue')

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
    if not request.user.is_authenticated:
        return redirect('/landing/')
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now() - timedelta(days=2)
        selected_actor = get_object_or_404(Actor, pk=actor_id)
        ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
                                                    movieId__movieId = OuterRef('pk'),
                                                    movieStartTime = None).values('movieStartTime')
        ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
                                                    movieId__movieId = OuterRef('pk'), 
                                                    movieStartTime__gte = twoDaysAgo).values('movieStartTime')
        recValue = UserMovieStats.objects.filter(userId = current_user_object,
                                                movieId__movieId = OuterRef('pk')).values('recommendValue')
        movie_list = Movie.objects.filter(actors__actorId=actor_id).order_by('overallRating').annotate(
                                recValue=Subquery(recValue),
                                isUnwatched=Exists(ordersUnwatched),
                                startedWatching=Exists(ordersStarted)).order_by(
                                '-recValue')
        
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
    if not request.user.is_authenticated:
        return redirect('/landing/')
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now() - timedelta(days=2)
        selected_director = get_object_or_404(Director, pk=director_id)
        ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
                                                    movieId__movieId = OuterRef('pk'),
                                                    movieStartTime = None).values('movieStartTime')
        ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
                                                    movieId__movieId = OuterRef('pk'), 
                                                    movieStartTime__gte = twoDaysAgo).values('movieStartTime')
        recValue = UserMovieStats.objects.filter(userId = current_user_object,
                                                movieId__movieId = OuterRef('pk')).values('recommendValue')
        movie_list = Movie.objects.filter(directors__directorId=director_id).order_by('overallRating').annotate(
                                recValue=Subquery(recValue),
                                isUnwatched=Exists(ordersUnwatched),
                                startedWatching=Exists(ordersStarted)).order_by(
                                '-recValue')
        
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
    if not request.user.is_authenticated:
        return redirect('/landing/')
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now() - timedelta(days=2)
        selected_writer = get_object_or_404(Writer, pk=writer_id)
        ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
                                                    movieId__movieId = OuterRef('pk'),
                                                    movieStartTime = None).values('movieStartTime')
        ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
                                                    movieId__movieId = OuterRef('pk'), 
                                                    movieStartTime__gte = twoDaysAgo).values('movieStartTime')
        recValue = UserMovieStats.objects.filter(userId = current_user_object,
                                                movieId__movieId = OuterRef('pk')).values('recommendValue')
        movie_list = Movie.objects.filter(writers__writerId=writer_id).order_by('overallRating').annotate(
                                recValue=Subquery(recValue),
                                isUnwatched=Exists(ordersUnwatched),
                                startedWatching=Exists(ordersStarted)).order_by(
                                '-recValue')
        
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
