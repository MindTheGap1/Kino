from django.shortcuts import render, get_object_or_404, redirect
from django.core.management import call_command
from django.http import HttpResponse
from django.db.models import Exists, OuterRef, Subquery, Count, Sum, Value, Max
from search.forms import SearchForm
from movies.forms import RatingForm
from cart.forms import CartAddProductForm
from account.models import UserMovieStats, User
from django.contrib.auth.models import User as Auth_User
from datetime import datetime, timedelta
from .models import *
from orders.models import OrderItem, Order
import pytz
import math

def index(request,page_no=1):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    #if user has not completed cold-start
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        if User.objects.filter(user_id = user_id):
            if User.objects.get(user_id = user_id).completedTutorial == False:
                return redirect('/genre/')
        else:
            User.objects.create(user_id = user_id, completedTutorial = False)
            return redirect('/genre/')


        twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
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
        page_total = math.ceil(len(movie_list) / 15)
        movie_list = movie_list[(page_no - 1) * 15:page_no * 15]
        

        genre_list = Genre.objects.order_by('genreName')
        search_form = SearchForm

        template = 'movies/index.html'
        context = {
            'movie_list': movie_list,
            'genre_list': genre_list,
            'search_form': search_form,
            'page_no': page_no,
            'page_total': page_total,
        }
        return render(request, template, context)

def detail(request, movie_id):
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

        movie = get_object_or_404(Movie, pk=movie_id)
        current_user_object = Auth_User.objects.get(pk=user_id)
        link = movie.trailerLink
        pos = link.find('?v=')
        vidId = link[pos + 3: len(link)]
        form = RatingForm(request.POST)
        match = UserMovieStats.objects.filter(userId=current_user_object, movieId = movie)
        if form.is_valid():
            if not match:
                #User is rating for first time
                post = form.save(commit=False)
                post.userId = current_user_object
                post.movieId = movie
                post.lastRating = datetime.now(pytz.UTC)
                post.save()
                call_command('getratings', movie_id=[movie.movieId])
                call_command('getrecommends', user_id=[current_user_object.id])
                movie = get_object_or_404(Movie, pk=movie_id)
            else:
                match[0].userId = current_user_object
                match[0].movieId = movie
                match[0].rating = form.cleaned_data['rating']
                match[0].lastRating = datetime.now(pytz.UTC)
                match[0].save()
                call_command('getratings', movie_id=[movie.movieId])
                call_command('getrecommends', user_id=[current_user_object.id])
                movie = get_object_or_404(Movie, pk=movie_id)


        if match:
            if match[0].rating:
                filmRating = int(match[0].rating)
            else:
                filmRating = 0
        else:
            filmRating = 0

        cart_form = CartAddProductForm()
        template = 'movies/detail.html'
        context = {
            'movie': movie,
            'vidId': vidId,
            'form': form,
            'cart_form': cart_form,
            'rating': filmRating,
        }
        return render(request, template, context)


def popular(request):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    #if user has not completed cold-start
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        if User.objects.filter(user_id = user_id):
            if User.objects.get(user_id = user_id).completedTutorial == False:
                return redirect('/genre/')
        else:
            User.objects.create(user_id = user_id, completedTutorial = False)
            return redirect('/genre/')


        twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
        sevenDaysAgo = datetime.now(pytz.UTC) - timedelta(days=7)
        ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
                                                    movieId__movieId = OuterRef('pk'),
                                                    movieStartTime = None).values('movieStartTime')
        ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
                                                    movieId__movieId = OuterRef('pk'), 
                                                    movieStartTime__gte = twoDaysAgo).values('movieStartTime')
        movie_list = Movie.objects.annotate(
                                isUnwatched=Exists(ordersUnwatched),
                                startedWatching=Exists(ordersStarted),
                                )

        ratings_movie_list = sorted(movie_list, key=lambda i: i.get_ratings(), reverse=True)[:5]
        orders_movie_list = sorted(movie_list, key=lambda i: i.get_orders(), reverse=True)[:5]

        genre_list = Genre.objects.order_by('genreName')
        search_form = SearchForm

        template = 'movies/popular.html'
        context = {
            'ratings_movie_list': ratings_movie_list,
            'orders_movie_list': orders_movie_list,
            'genre_list': genre_list,
            'search_form': search_form,
        }
        return render(request, template, context)

def popular_orders(request, page_no=1):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    #if user has not completed cold-start
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        if User.objects.filter(user_id = user_id):
            if User.objects.get(user_id = user_id).completedTutorial == False:
                return redirect('/genre/')
        else:
            User.objects.create(user_id = user_id, completedTutorial = False)
            return redirect('/genre/')


        twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
        sevenDaysAgo = datetime.now(pytz.UTC) - timedelta(days=7)
        ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
                                                    movieId__movieId = OuterRef('pk'),
                                                    movieStartTime = None).values('movieStartTime')
        ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
                                                    movieId__movieId = OuterRef('pk'), 
                                                    movieStartTime__gte = twoDaysAgo).values('movieStartTime')
        movie_list = Movie.objects.annotate(
                                isUnwatched=Exists(ordersUnwatched),
                                startedWatching=Exists(ordersStarted),
                                )

        orders_movie_list = sorted(movie_list, key=lambda i: i.get_orders(), reverse=True)
        page_total = math.ceil(len(orders_movie_list) / 15)
        orders_movie_list = orders_movie_list[(page_no - 1) * 15:page_no * 15]

        genre_list = Genre.objects.order_by('genreName')
        search_form = SearchForm

        template = 'movies/popular_orders.html'
        context = {
            'movie_list': orders_movie_list,
            'genre_list': genre_list,
            'search_form': search_form,
            'page_no': page_no,
            'page_total': page_total,
        }
        return render(request, template, context)

def popular_ratings(request, page_no=1):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    #if user has not completed cold-start
    else:
        user_id = request.user.id
        current_user_object = Auth_User.objects.get(id=user_id)
        if User.objects.filter(user_id = user_id):
            if User.objects.get(user_id = user_id).completedTutorial == False:
                return redirect('/genre/')
        else:
            User.objects.create(user_id = user_id, completedTutorial = False)
            return redirect('/genre/')


        twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
        sevenDaysAgo = datetime.now(pytz.UTC) - timedelta(days=7)
        ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
                                                    movieId__movieId = OuterRef('pk'),
                                                    movieStartTime = None).values('movieStartTime')
        ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
                                                    movieId__movieId = OuterRef('pk'), 
                                                    movieStartTime__gte = twoDaysAgo).values('movieStartTime')
        movie_list = Movie.objects.annotate(
                                isUnwatched=Exists(ordersUnwatched),
                                startedWatching=Exists(ordersStarted),
                                )

        ratings_movie_list = sorted(movie_list, key=lambda i: i.get_ratings(), reverse=True)
        page_total = math.ceil(len(ratings_movie_list) / 15)
        ratings_movie_list = ratings_movie_list[(page_no - 1) * 15:page_no * 15]

        genre_list = Genre.objects.order_by('genreName')
        search_form = SearchForm

        template = 'movies/popular_ratings.html'
        context = {
            'movie_list': ratings_movie_list,
            'genre_list': genre_list,
            'search_form': search_form,
            'page_no': page_no,
            'page_total': page_total,
        }
        return render(request, template, context)

def genre_detail(request, genre_id, page_no=1):
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
        
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
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

        page_total = math.ceil(len(movie_list) / 15)
        movie_list = movie_list[(page_no - 1) * 15:page_no * 15]

        genre_list = Genre.objects.order_by('genreName')
        search_form = SearchForm

        template = 'movies/genre_detail.html'
        context = {
            'current_id': genre_id,
            'selected_genre': selected_genre,
            'movie_list': movie_list,
            'genre_list': genre_list,
            'search_form': search_form,
            'page_no': page_no,
            'page_total': page_total,
        }
        return render(request, template, context)

def actor_detail(request, actor_id, page_no=1):
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
        
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
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
        page_total = math.ceil(len(movie_list) / 15)
        movie_list = movie_list[(page_no - 1) * 15:page_no * 15]
        
        genre_list = Genre.objects.order_by('genreName')
        search_form = SearchForm

        template = 'movies/actor_detail.html'
        context = {
            'current_id': actor_id,
            'selected_actor': selected_actor,
            'movie_list': movie_list,
            'genre_list': genre_list,
            'search_form': search_form,
            'page_no': page_no,
            'page_total': page_total,
        }
        return render(request, template, context)

def director_detail(request, director_id, page_no=1):
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
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
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
        
        page_total = math.ceil(len(movie_list) / 15)
        movie_list = movie_list[(page_no - 1) * 15:page_no * 15]

        genre_list = Genre.objects.order_by('genreName')
        search_form = SearchForm

        template = 'movies/director_detail.html'
        context = {
            'current_id': director_id,
            'selected_director': selected_director,
            'movie_list': movie_list,
            'genre_list': genre_list,
            'search_form': search_form,
            'page_no': page_no,
            'page_total': page_total,
        }
        return render(request, template, context)

def writer_detail(request, writer_id, page_no=1):
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
        current_user_object = Auth_User.objects.get(id=user_id)
        twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
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
        
        page_total = math.ceil(len(movie_list) / 15)
        movie_list = movie_list[(page_no - 1) * 15:page_no * 15]

        genre_list = Genre.objects.order_by('genreName')
        search_form = SearchForm

        template = 'movies/writer_detail.html'
        context = {
            'current_id': writer_id,
            'selected_writer': selected_writer,
            'movie_list': movie_list,
            'genre_list': genre_list,
            'search_form': search_form,
            'page_no': page_no,
            'page_total': page_total,
        }
        return render(request, template, context)
