from account.models import User as User_Profile
from .models import Order, OrderItem
from movies.models import Movie, Genre
from account.models import User
from search.forms import SortForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as Auth_User
from django.db.models import Q, Count, Max, Min, Exists, OuterRef, Subquery, Value
from datetime import datetime, timedelta
from cart.cart import Cart
import pytz

def checkout(request):
	#THIS IS NOT THE ACTUAL CHECKOUT
	#THIS IS FOR THE SAKE OF DEMONSTRATING
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

		current_user_object = Auth_User.objects.get(id=request.user.id)
		cart = Cart(request)
		order = Order(userId = current_user_object, paid=True,
					card_number=str(1), cardholder_name="test",
					expiry_date="1/1", CVV_code=str(111))

		order.save()
		for item in cart:
			order_item = OrderItem(orderId=order, movieId=item['movie'], cost=item['price'])
			order_item.save()
		cart.clear()
		
		return redirect('/')



def order_list(request):
	if request.user.is_authenticated:
		user_id = request.user.id
		if User.objects.filter(user_id = user_id):
			if User.objects.get(user_id = user_id).completedTutorial == False:
				return redirect('/genre/')
		else:
			User.objects.create(user_id = user_id, completedTutorial = False)
			return redirect('/genre/')


		current_user_object = Auth_User.objects.get(id=user_id)
		all_orders = Order.objects.filter(userId=current_user_object)
		all_order_items = OrderItem.objects.filter(Q(orderId__in=all_orders))
		
		sort_select = int(request.POST.get("sort_select")) if request.POST.get("sort_select") != None else 0
		sorting_list = ['movieName', '-movieName', 'price', '-price', 'overallRating', '-overallRating', 'length', '-length', 'releaseDate', '-releaseDate']

		twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
		two_days = timedelta(days=2)
		movie_list = Movie.objects.filter(Q(order__in=all_order_items)).order_by(sorting_list[sort_select]).annotate(
								numOrders=Count('movieId'),
								latestOrder=Max('order__orderId__orderCreated'),
								latestWatch=Max('order__movieStartTime'),
								isUnwatched=Count('order', filter=Q(order__movieStartTime = None)),
								startedWatching=Count('order', filter=Q(order__movieStartTime__gte = twoDaysAgo )))

		

		unwatched_list, started_list = [], []
		for movie in movie_list:
			if movie.startedWatching > 0:
				started_list += [movie]	
			if movie.isUnwatched > 0:
				unwatched_list += [movie]

		sort_form = SortForm()
		#test = a()
		context = {
	        'movie_list': movie_list,
	        'started_list': started_list,
	        'unwatched_list': unwatched_list,
	        'two_days': two_days,
	        'sort_form': sort_form,
		}
		template = "orders/index.html"
		return render(request, template, context)
	else:
		return redirect('/landing')


def watch(request, movie_id):
	if request.user.is_authenticated:
		user_id = request.user.id
		if User.objects.filter(user_id = user_id):
			if User.objects.get(user_id = user_id).completedTutorial == False:
				return redirect('/genre/')
		else:
			User.objects.create(user_id = user_id, completedTutorial = False)
			return redirect('/genre/')
			
		current_user_object = Auth_User.objects.get(id=user_id)
		twoDaysAgo = datetime.now(pytz.UTC) - timedelta(days=2)
		ordersUnwatched = OrderItem.objects.filter(orderId__userId = current_user_object,
													movieId__movieId = OuterRef('pk'),
													movieStartTime = None).values('movieStartTime')
		ordersStarted = OrderItem.objects.filter(orderId__userId = current_user_object, 
													movieId__movieId = OuterRef('pk'), 
													movieStartTime__gte = twoDaysAgo).values('movieStartTime')
		movie = Movie.objects.filter(movieId=movie_id).annotate(
							isUnwatched=Exists(ordersUnwatched),
							startedWatching=Exists(ordersStarted),
							latestWatch=Max('order__movieStartTime'))
		x = movie[0].startedWatching
		y = movie[0].isUnwatched
		if not movie[0].startedWatching and not movie[0].isUnwatched:
			return redirect('/')

		if movie[0].isUnwatched and not movie[0].startedWatching:
			latest_film = OrderItem.objects.filter(Q(movieId=movie_id) & Q(movieStartTime = None) & Q(orderId__userId = current_user_object)).latest('-orderId__orderCreated')
			latest_film.movieStartTime = datetime.now(pytz.UTC)
			latest_film.save(update_fields=['movieStartTime'])


		two_days = timedelta(days=2)
		context = {
			'movie': movie[0],
			'two_days': two_days,
		}
		template = "orders/watch.html"
		return render(request, template, context)
	else:
		return redirect('/landing')


def order_history(request):
	if request.user.is_authenticated:
		user_id = request.user.id
		if User.objects.filter(user_id = user_id):
			if User.objects.get(user_id = user_id).completedTutorial == False:
				return redirect('/genre/')
		else:
			User.objects.create(user_id = user_id, completedTutorial = False)
			return redirect('/genre/')
			
		current_user_object = Auth_User.objects.get(id=user_id)
		orders = Order.objects.filter(userId=current_user_object)

		order_info_list = []
		for order in orders:
			order_info_list += OrderItem.objects.filter(orderId=order.orderId)

		template = 'orders/orders.html'
		context = {
			'orders': orders,
			'order_info_list': order_info_list,
		}
		return render(request, template, context)
	else:
		return redirect('/landing')