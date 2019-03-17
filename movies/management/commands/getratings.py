from django.core.management.base import BaseCommand, CommandError
from decimal import Decimal
from movies.models import Movie
from account.models import UserMovieStats

class Command(BaseCommand):
	help = 'Gathers all user ratings for a movie (or all movies if none specified) and puts them into the overall ratings field for that movie'

	def add_arguments(self, parser):
		parser.add_argument('-id', dest='movie_id', nargs='+', type=int, help = 'Indicates the Movie(s) to be updated, leave blank to do all movies')

	def handle(self, *args, **options):
		if options['movie_id']:
			for movie_id in options['movie_id']:
				movie = Movie.objects.get(movieId=movie_id)
				ratings = UserMovieStats.objects.filter(movieId=movie).values_list('rating', flat=True)
				ratings = list(filter(None, ratings))
				if ratings:
					overallRating = sum(ratings)/len(ratings)
					if movie.overallRating:
						existingRating = movie.overallRating
					else:
						existingRating = 0
					if abs(existingRating - Decimal(overallRating)) > 0.005:
						movie.overallRating = overallRating
						movie.save()
						self.stdout.write("Updated ratings for " + movie.movieName)
				else:
					self.stdout.write("No ratings for " + movie.movieName)
		else:
			movie_list = Movie.objects.all()
			for movie in movie_list:
				ratings = UserMovieStats.objects.filter(movieId=movie).values_list('rating', flat=True)
				ratings = list(filter(None, ratings))
				if ratings:
					overallRating = sum(ratings)/len(ratings)
					if movie.overallRating:
						existingRating = movie.overallRating
					else:
						existingRating = 0
					if abs(existingRating - Decimal(overallRating)) > 0.005:
						movie.overallRating = overallRating
						movie.save()
						self.stdout.write("Updated ratings for " + movie.movieName)

