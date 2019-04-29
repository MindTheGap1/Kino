from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from movies.models import Movie
from account.models import User
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    else:
        cart = Cart(request)
        movie = get_object_or_404(Movie, movieId=movie_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(movie=movie,
                     update_quantity=cd['update'])
        return redirect('cart:cart_detail')


def cart_remove(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    else:
        cart = Cart(request)
        movie = get_object_or_404(Movie, movieId=movie_id)
        cart.remove(movie)
        return redirect('cart:cart_detail')


def cart_detail(request):
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
            
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                       'update': True})
        context = {
            'cart': cart,
        }
        template = 'cart/detail.html'
        return render(request, template, context)
