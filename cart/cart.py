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
        Iterate over the items in the cart and get the 'movies' from the database.
        """
        movie_ids = self.cart.keys()
        # get the 'movies' objects and add them to the cart
        movie_list = Movies.objects.filter(id__in = movie_ids)
        for movies in movie_list:
            self.cart[str(movies.movieId)]['movies'] = movies

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, movies, quantity=1, update_quantity=False):
        """
        Add a 'Movies' to the cart or update its quantity.
        """
        movieIds = str(movies.movieId)
        if movies_id not in self.cart:
            self.cart[movieIds] = {'quantity': 0,
                                      'price': str(movies.price)}
        if update_quantity:
            self.cart[movieIds]['quantity'] = quantity
        else:
            self.cart[movieIds]['quantity'] += quantity
        self.save()

    def remove(self, movies):
        """
        Remove a 'Movies' from the cart.
        """
        movieIds = str(movies.movieId)
        if movieIds in self.cart:
            del self.cart[movieIds]
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

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
