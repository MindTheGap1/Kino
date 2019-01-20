from django.db import models


class Movies(models.Model):
    movieId = models.AutoField(primary_key=True)
    movieName = models.CharField(max_length=200)
    description = models.TextField()
    length = models.DurationField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    trailerLink = models.CharField(max_length=100)
    image = models.ImageField(upload_to='img', blank=True)
    noRents = models.PositiveIntegerField()
    addedDate = models.DateTimeField(auto_now_add=True)
    overallRating = models.DecimalField(decimal_places=2, max_digits=4)
    ageRating = models.CharField(max_length=3)

    def __str__(self):
        return self.movieName

    def get_absolute_url(self):
        return reverse('movies:movie_detail', args=[self.movieId])


class Actors(models.Model):
    actorId = models.AutoField(primary_key=True)
    actorFirstName = models.CharField(max_length=100)
    actorLastName = models.CharField(max_length=100)

    def __str__(self):
        return self.actorFirstName + " " + self.actorLastName

class Genres(models.Model):
    genreId = models.AutoField(primary_key=True)
    genreName = models.CharField(max_length=200)

    def __str__(self):
        return self.genreName

class Directors(models.Model):
    directorId = models.AutoField(primary_key=True)
    directorFirstName = models.CharField(max_length=100)
    directorLastName = models.CharField(max_length=100)

    def __str__(self):
        return self.directorFirstName + " " + directorLastName

class Writers(models.Model):
    writerId = models.AutoField(primary_key=True)
    writerFirstName = models.CharField(max_length=100)
    writerLastName = models.CharField(max_length=100)

    def __str__(self):
        return self.writerFirstName + " " + writerLastName


class MovieActors(models.Model):
    movieId = models.ForeignKey(Movies, related_name='actors', on_delete=models.CASCADE)
    actorId = models.ForeignKey(Actors, related_name='movies', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movieId', 'actorId')

class MovieGenres(models.Model):
    movieId = models.ForeignKey(Movies, related_name='genres', on_delete=models.CASCADE)
    genreId = models.ForeignKey(Genres, related_name='movies', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movieId', 'genreId')    

class MovieDirectors(models.Model):
    movieId = models.ForeignKey(Movies, related_name='directors', on_delete=models.CASCADE)
    directorId = models.ForeignKey(Directors, related_name='movies', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movieId', 'directorId')

class MovieWriters(models.Model):
    movieId = models.ForeignKey(Movies, related_name='writers', on_delete=models.CASCADE)
    writerId = models.ForeignKey(Writers, related_name='movies', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movieId', 'writerId')