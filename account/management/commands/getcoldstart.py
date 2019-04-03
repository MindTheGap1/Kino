from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User as Auth_User
from account.models import UserMovieStats, FavouriteGenres
from movies.models import Movie, Genre, Actor, Writer, Director
from django.db.models import Q
import numpy as np
import math

class Command(BaseCommand):
	help = 'Gathers all the values for recommending movies (or specific movies) to users (or specific users). Done by Cosine Similarity.'

	def add_arguments(self, parser):
		parser.add_argument('-u', '--user', dest='user_id', nargs='+', type=int, help = 'Indicates the User(s) to be updated, leave blank to do all users')
		parser.add_argument('-m', '--movie', dest='movie_id', nargs='+', type=int, help = 'Indicates the Movie(s) to be updated, leave blank to do all movies')

	def handle(self, *args, **options):
		all_movies = Movie.objects.all()
		all_genres = Genre.objects.all()
		all_users = Auth_User.objects.all()

		if options['movie_id']:
			movie_list = Movie.objects.filter(pk__in=options['movie_id'])
		else:
			movie_list = Movie.objects.all()

		if options['user_id']:
			user_list = Auth_User.objects.filter(pk__in=options['user_id'])
		else:
			user_list = Auth_User.objects.all()


		movie_genres_dict = {}
		user_genres_dict = {}

		for movie in all_movies:
			genre_list =  []
			for genre in all_genres:
				if genre.genreId in movie.genres.values_list('genreId',flat=True):
					genre_list += [1]
				else:
					genre_list += [0]

			movie_genres_dict[movie.movieId] = genre_list


		for user in all_users:
			genre_list = []
			for genre in all_genres:
				if genre.genreId in user.favouritegenres.values_list('genreId_id', flat=True):
					genre_list += [1]
				else:
					genre_list += [0]
			user_genres_dict[user.id] = genre_list

		user_movie_genres_adj = self.get_adj_dict(user_genres_dict, movie_genres_dict)


		for u, user_u in enumerate(user_list):
			for i, movie_i in enumerate(movie_list):
				value = 0
				full_list = user_movie_genres_adj[user_u.id]
				for j, movie_j in enumerate(all_movies):
					if movie_i == movie_j:
						value = full_list[j]

				userstats_value = user_u.moviestats.filter(Q(movieId__movieId = movie_i.movieId) & Q(userId__id = user_u.id))
				if userstats_value:
					userstats_value[0].recommendValue = value
					userstats_value[0].save()
				else:
					usv = UserMovieStats(movieId = movie_i, userId = user_u, recommendValue = value)
					usv.save()
				




	def get_adj_dict(self, in_dict1, in_dict2={}):
		if in_dict2 == {}:
			in_dict2 = in_dict1
		adj_dict = {}
		for key_i, value_i in in_dict1.items():
			list = []
			#self.stdout.write(str(key_i))
			for key_j, value_j in in_dict2.items():
				recValue = None
				if key_i != key_j:
					#self.stdout.write("\t" + str(value_i) + " vs " + str(value_j))
					norm_i = np.linalg.norm(value_i)
					norm_j = np.linalg.norm(value_j)
					if norm_i != 0 and norm_j != 0:
						cosTheta = np.dot(value_i, value_j) / (norm_i * norm_j)
						if cosTheta > 1:
							cosTheta = 1;
						theta = math.degrees(math.acos(cosTheta))
						recValue = 5 - theta * (5/90)
						list += [recValue]
						#self.stdout.write("\t" + str(key_i) + " vs " + str(key_j))
						#self.stdout.write("\t\t" + str(recValue))
				if recValue == None:
					list += [0.0]
			adj_dict[key_i] = list
		return adj_dict
