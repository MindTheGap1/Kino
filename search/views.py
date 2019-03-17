from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User as Auth_User
from movies.models import Movie, Genre
from orders.models import OrderItem
from account.models import UserMovieStats
from django.db.models import Exists, OuterRef, Subquery
from datetime import datetime, timedelta
from functools import reduce
import operator
from .forms import SearchForm

def searchMovie(request):
	if not request.user.is_authenticated:
		return redirect('/landing/')
	else:
		user_id = request.user.id
		current_user_object = Auth_User.objects.get(id=user_id)
		phrase = request.POST.get("phrase") if request.POST.get("phrase") != "" else "" #Stops it displaying "None"
		genre_select = request.POST.get("genre_select")
		sort_select = int(request.POST.get("sort_select")) if request.POST.get("sort_select") != None else 0
		movie_list, new_movie_list = [], []
		sorting_list = ['movieName', '-movieName', 'price', '-price', 'overallRating', '-overallRating', 'length', '-length', 'releaseDate', '-releaseDate']
		twoDaysAgo = datetime.now() - timedelta(days=2)

		ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
												movieId__movieId = OuterRef('pk'),
												movieStartTime = None).values('movieStartTime')
		ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
												movieId__movieId = OuterRef('pk'), 
												movieStartTime__gte = twoDaysAgo).values('movieStartTime')
		recValue = UserMovieStats.objects.filter(userId = current_user_object,
												movieId__movieId = OuterRef('pk')).values('recommendValue')

		if phrase:
			phrase = phrase.strip()
			phrase_sep = phrase.split(" ")

			
			movie_list = Movie.objects.filter(	reduce(operator.or_, (Q(movieName__icontains=word) for word in phrase_sep))
												| reduce(operator.or_, (Q(description__icontains=word) for word in phrase_sep))
												| reduce(operator.or_, (Q(actors__actorFirstName__icontains=word) for word in phrase_sep))
												| reduce(operator.or_, (Q(actors__actorLastName__icontains=word) for word in phrase_sep))
												| reduce(operator.or_, (Q(writers__writerFirstName__icontains=word) for word in phrase_sep))
												| reduce(operator.or_, (Q(writers__writerLastName__icontains=word) for word in phrase_sep))
												| reduce(operator.or_, (Q(directors__directorFirstName__icontains=word) for word in phrase_sep))
												| reduce(operator.or_, (Q(directors__directorLastName__icontains=word) for word in phrase_sep))
												| reduce(operator.or_, (Q(genres__genreName__icontains=word) for word in phrase_sep))).distinct().annotate(
												recValue=Subquery(recValue),
												isUnwatched=Exists(ordersUnwatched),
												startedWatching=Exists(ordersStarted)).order_by(sorting_list[sort_select], '-recValue')
		else:
			movie_list = Movie.objects.order_by('movieName').annotate(
												recValue=Subquery(recValue),
												isUnwatched=Exists(ordersUnwatched),
												startedWatching=Exists(ordersStarted)).order_by(sorting_list[sort_select], '-recValue')


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