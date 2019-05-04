from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User as Auth_User
from account.models import UserMovieStats, FavouriteGenres
from movies.models import Movie, Genre, Actor, Writer, Director
from django.db.models import Q
import numpy as np
import math

class Command(BaseCommand):
	help = 'Gathers all the values for recommending movies (or specific movies) to users (or specific users). Done by Cosine Similarity by default.'

	def add_arguments(self, parser):
		parser.add_argument('-u', '--user', dest='user_id', nargs='+', type=int, help = 'Indicates the User(s) to be updated, leave blank to do all users')
		parser.add_argument('-m', '--movie', dest='movie_id', nargs='+', type=int, help = 'Indicates the Movie(s) to be updated, leave blank to do all movies')
		parser.add_argument('-s', '--similarity', dest='similarity', help = 'Indicates what correlation to use: \'P\' for Pearson\'s Correlation, \'C\' for Cosine Similarity')

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

		user_genres_dict = {}
		user_genres_adj = {}

		user_ratings_dict, movie_ratings_dict = {}, {}
		user_ratings_adj= {}

		for movie in all_movies:
			rating_list = []
			for user in all_users:
				userstats_value = user.moviestats.filter(Q(movieId__movieId = movie.movieId) & Q(userId__id = user.id))
				if userstats_value:
					rating = userstats_value.values_list('rating', flat=True)
					if rating[0]:
						rating_list += [rating[0]]
					else:
						rating_list += [0]
				else:
					rating_list += [0]

			movie_ratings_dict[movie.movieId] = rating_list

		users_ratings_avg = {}
		for user in all_users:
			rating_list = []
			genre_list = []
			rating_sum = 0
			rating_count = 0
			for movie in all_movies:
				userstats_value = user.moviestats.filter(Q(movieId__movieId = movie.movieId) & Q(userId__id = user.id))
				if userstats_value:
					rating = userstats_value.values_list('rating', flat=True)
					if rating[0]:
						rating_list += [rating[0]]
						rating_sum += rating[0]
						rating_count += 1
					else:
						rating_list += [0]
				else:
					rating_list += [0]

			for genre in all_genres:
				if genre.genreId in user.favouritegenres.values_list('genreId_id', flat=True):
					genre_list += [1]
				else:
					genre_list += [0]
			user_ratings_dict[user.id] = rating_list
			user_genres_dict[user.id] = genre_list
			if rating_count > 0:
				users_ratings_avg[user.id] = rating_sum / rating_count
			else:
				users_ratings_avg[user.id] = 0


		user_ratings_adj = self.get_adj_dict(user_ratings_dict)
		user_genres_adj = self.get_adj_dict(user_genres_dict)

		total_user_adj = {}
		user_ratings_pearsons = {}

		for u, user_u in enumerate(all_users):
			list = []
			for j in range(len(all_users)):
				ratings_val = user_ratings_adj[user_u.id][j]
				genres_val = user_genres_adj[user_u.id][j]
				list += [5/10 * (genres_val + ratings_val)]
			total_user_adj[user_u.id] = list

			rlist = []
			for v, user_v in enumerate(all_users):
				#https://www.analyticsvidhya.com/blog/2018/06/comprehensive-guide-recommendation-engine-python/
				sum_uv = 0
				sum_u_sq = 0
				sum_v_sq = 0
				for movie in all_movies:
					if movie_ratings_dict[movie.movieId][u] > 0 and movie_ratings_dict[movie.movieId][v] > 0:
						sum_uv += (movie_ratings_dict[movie.movieId][u] - users_ratings_avg[user_u.id]) * (movie_ratings_dict[movie.movieId][v] - users_ratings_avg[user_v.id])
						sum_u_sq += (movie_ratings_dict[movie.movieId][u] - users_ratings_avg[user_u.id])**2
						sum_v_sq += (movie_ratings_dict[movie.movieId][v] - users_ratings_avg[user_v.id])**2

				if sum_u_sq == 0 or sum_v_sq == 0:
					r = 0 + 0.1 * user_genres_adj[user_u.id][v]
				else:
					r = 0.9* (sum_uv / (math.sqrt(sum_u_sq) * math.sqrt(sum_v_sq))) + (0.1/5) * user_genres_adj[user_u.id][v]
				rlist += [r]
			user_ratings_pearsons[user_u.id] = rlist

		recommend_dict = {}

		for user_u in user_list:
			list = []
			for movie in movie_list:
				rating = None
				sum_rating_adj = 0
				sum_adj = 0
				userstats_value = user_u.moviestats.filter(Q(movieId__movieId = movie.movieId) & Q(userId__id = user_u.id))

				for v, user_v in enumerate(all_users):
					if user_v != user_u:
						if options['similarity'] == "C":
							sum_rating_adj += movie_ratings_dict[movie.movieId][v] * total_user_adj[user_u.id][v]
							sum_adj += total_user_adj[user_u.id][v]
						else:
							sum_rating_adj += movie_ratings_dict[movie.movieId][v] * user_ratings_pearsons[user_u.id][v]
							sum_adj += user_ratings_pearsons[user_u.id][v]
				if sum_adj == 0:
					predicted_rating = 0
				else:
					predicted_rating = sum_rating_adj / sum_adj

				if userstats_value:
					rating = userstats_value.values_list('rating', flat=True)[0]
					if rating:
						if rating > 2.5:
							predicted_rating = predicted_rating * (0.5 + (0.2 * (rating - 2.5)))
						else:
							predicted_rating = predicted_rating * (0.5 - 0.2 * (2.5 - rating))

				list += [predicted_rating]

			if options['similarity'] != "C":
				range_vals = max( abs(max(x for x in list if x is not None)), abs(min(x for x in list if x is not None)) )

			for i, movie in enumerate(movie_list):
				if options['similarity'] != "C":
					if range_vals == 0:
						list[i] = 0
					else:
						list[i] = (list[i] + range_vals) * (5 / (range_vals * 2))

				userstats_value = user_u.moviestats.filter(Q(movieId__movieId = movie.movieId) & Q(userId__id = user_u.id))
				if userstats_value:
					userstats_value[0].recommendValue = list[i]
					userstats_value[0].save()
				else:
					usv = UserMovieStats(movieId = movie, userId = user_u, recommendValue = list[i])
					usv.save()

			recommend_dict[user_u.id] = list




	def get_adj_dict(self, in_dict):
		adj_dict = {}
		for key_i, value_i in in_dict.items():
			list = []
			for key_j, value_j in in_dict.items():
				recValue = None
				if key_i != key_j:
					norm_i = np.linalg.norm(value_i)
					norm_j = np.linalg.norm(value_j)
					if norm_i != 0 and norm_j != 0:
						cosTheta = np.dot(value_i, value_j) / (norm_i * norm_j)
						if cosTheta > 1:
							cosTheta = 1;
						theta = math.degrees(math.acos(cosTheta))
						recValue = 5 - theta * (5/90)
						list += [recValue]
				if recValue == None:
					list += [0.0]
			adj_dict[key_i] = list
		return adj_dict
