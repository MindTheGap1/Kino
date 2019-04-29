from decimal import Decimal
from django.conf import settings
from movies.models import Movie


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the movie from the database.
        """
        movie_ids = self.cart.keys()
        # get the movie objects and add them to the cart
        movies = Movie.objects.filter(movieId__in = movie_ids)
        for movie in movies:
            self.cart[str(movie.movieId)]['movie'] = movie

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, movie, update_quantity=False):
        """
        Add a movie to the cart or update its quantity.
        """
        movie_id = str(movie.movieId)
        if movie_id not in self.cart:
            self.cart[movie_id] = {'quantity': 1,
                                      'price': str(movie.price)}
        if update_quantity:
            self.cart[movie_id]['quantity'] = quantity
        else:
            self.cart[movie_id]['quantity'] = 1
        self.save()

    def remove(self, movie):
        """
        Remove a movie from the cart.
        """
        movie_id = str(movie.movieId)
        if movie_id in self.cart:
            del self.cart[movie_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def count(self):
        if(self.__len__() < 1):
            return ""
        else:
            return "(" + str(self.__len__()) + ")"

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
