from django.db import models
from django.contrib.auth.models import User as Auth_User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
#from phonenumber_field.modelfields import PhoneNumberField
from movies.models import Movie, Genre


class User(models.Model):
    user = models.OneToOneField(Auth_User, on_delete=models.CASCADE)
    dob = models.DateField(auto_now_add=True)
    profilePic = models.ImageField(upload_to='profile_img', blank=True)
    #mobileNumber = PhoneNumberField()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class UserMovieStats(models.Model):
    userId = models.ForeignKey(User, related_name='moviestats', on_delete=models.CASCADE)
    movieId = models.ForeignKey(Movie, related_name='userstats', on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    lastWatchPos = models.DurationField()
    allowRecommend = models.BooleanField(default=True)

class FavouriteGenres(models.Model):
    userId = models.ForeignKey(Auth_User, related_name='favouritegenres', on_delete=models.CASCADE)
    genreId = models.ForeignKey(Genres, related_name='usersfavourite', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('userId', 'genreId')
