from django.urls import reverse
from django.db import models
from datetime import datetime, timedelta
import pytz

class Movie(models.Model):
    movieId = models.AutoField(primary_key=True)
    movieName = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    length = models.DurationField(null=True,blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20,null=True,blank=True)
    trailerLink = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to='img',null=True,blank=True)
    noRents = models.PositiveIntegerField(null=True,blank=True)
    releaseDate = models.DateField(null=True,blank=True)
    addedDate = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    overallRating = models.DecimalField(decimal_places=2, max_digits=4,null=True,blank=True)
    ageRating = models.CharField(max_length=3,null=True,blank=True)
    actors = models.ManyToManyField('Actor',blank=True, related_name='movies')
    genres = models.ManyToManyField('Genre',blank=True, related_name='movies')
    directors = models.ManyToManyField('Director',blank=True, related_name='movies')
    writers = models.ManyToManyField('Writer',blank=True, related_name='movies')

    def __str__(self):
        return self.movieName

    def get_absolute_url(self):
        return reverse('movies:detail', args=[self.movieId])

    def get_ratings(self):
        sevenDaysAgo = datetime.now(pytz.UTC) - timedelta(days=7)
        weeksRatings = Movie.objects.filter(userstats__movieId=self,
                                                userstats__lastRating__gte=sevenDaysAgo,
                                                userstats__rating__gte=3).values('userstats').count()
        return weeksRatings

    def get_orders(self):
        sevenDaysAgo = datetime.now(pytz.UTC) - timedelta(days=7)
        weeksOrders = Movie.objects.filter(order__movieId=self,
                                                order__orderId__orderCreated__gte=sevenDaysAgo).values('order').count()
        return weeksOrders


class Actor(models.Model):
    actorId = models.AutoField(primary_key=True)
    actorFirstName = models.CharField(max_length=100)
    actorLastName = models.CharField(max_length=100)

    def __str__(self):
        return self.actorFirstName + " " + self.actorLastName

class Genre(models.Model):
    genreId = models.AutoField(primary_key=True)
    genreName = models.CharField(max_length=200)

    def __str__(self):
        return self.genreName

class Director(models.Model):
    directorId = models.AutoField(primary_key=True)
    directorFirstName = models.CharField(max_length=100)
    directorLastName = models.CharField(max_length=100)

    def __str__(self):
        return self.directorFirstName + " " + self.directorLastName

class Writer(models.Model):
    writerId = models.AutoField(primary_key=True)
    writerFirstName = models.CharField(max_length=100)
    writerLastName = models.CharField(max_length=100)

    def __str__(self):
        return self.writerFirstName + " " + self.writerLastName
