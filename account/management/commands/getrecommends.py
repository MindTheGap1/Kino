from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User as Auth_User
from account.models import UserMovieStats, FavouriteGenres
from movies.models import Movie, Genres

class Command(BaseCommand):
	help = 'Gathers all the values for recommending movies to users (or specific user)'

	def add_arguments(self, parser):
		parser.add_argument('-user', dest='user_id', nargs='+', type=int, help = 'Indicates the User(s) to be updated, leave blank to do all users')
		parser.add_argument('-movie', dest='movie_id', nargs='+', type=int, help = 'Indicates the Movie(s) to be updated, leave blank to do all movies')

	def handle(self, *args, **options):
		all_movies = Movie.objects.all()
		if options['movie_id']:
			movie_list = Movie.objects.filter(pk__in=options['movie_id'])
		else:
			movie_list = Movie.objects.all()

		if options['user_id']:
			user_list = Auth_User.objects.filter(pk__in=options['user_id'])
		else:
			user_list = Auth_User.objects.all()

		self.stdout.write(str(user_list) + "\n" + str(movie_list))

		recommend_dict = {}



