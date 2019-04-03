from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=200)
    expiry_date = models.CharField(max_length=7)
    CVV_code = models.CharField(max_length=3)
    orderCreated = models.DateTimeField(auto_now_add=True)
    orderUpdated = models.DateTimeField(auto_now=True)
    
    def get_total_cost(self):
        return sum(movie.cost for movie in self.movies.all())

class OrderItem(models.Model):
    orderId = models.ForeignKey(Order, related_name='movies', on_delete=models.CASCADE)
    movieId = models.ForeignKey(Movie, related_name='order', on_delete=models.CASCADE)
    cost = models.DecimalField(decimal_places=2, max_digits=20)
    movieStartTime = models.DateTimeField(blank=True, null=True) # when the user first watches the movie
