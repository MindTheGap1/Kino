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
		all_writers = Writer.objects.all()
		all_directors = Director.objects.all()
		all_actors = Actor.objects.all()
		all_users = Auth_User.objects.all()

		if options['movie_id']:
			movie_list = Movie.objects.filter(pk__in=options['movie_id'])
		else:
			movie_list = Movie.objects.all()

		if options['user_id']:
			user_list = Auth_User.objects.filter(pk__in=options['user_id'])
		else:
			user_list = Auth_User.objects.all()

		#self.stdout.write(str(user_list) + "\n" + str(movie_list))

		movie_genres_dict, movie_writers_dict, movie_directors_dict, movie_actors_dict = {}, {}, {}, {}
		movie_genres_adj, movie_writers_adj, movie_directors_adj, movie_actors_adj = {}, {}, {}, {}
		user_genres_dict = {}
		user_genres_adj = {}

		user_ratings_dict, movie_ratings_dict = {}, {}
		user_ratings_adj, movie_ratings_adj = {}, {}

		for movie in all_movies:
			rating_list = []
			genre_list, actor_list, writer_list, director_list = [], [], [], []
			for genre in all_genres:
				if genre.genreId in movie.genres.values_list('genreId',flat=True):
					genre_list += [1]
				else:
					genre_list += [0]
			for writer in all_writers:
				if writer.writerId in movie.writers.values_list('writerId',flat=True):
					writer_list += [1]
				else:
					writer_list += [0]
			for director in all_directors:
				if director.directorId in movie.directors.values_list('directorId',flat=True):
					director_list += [1]
				else:
					director_list += [0]
			for actor in all_actors:
				if actor.actorId in movie.actors.values_list('actorId',flat=True):
					actor_list += [1]
				else:
					actor_list += [0]
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

			movie_genres_dict[movie.movieId] = genre_list
			movie_writers_dict[movie.movieId] = writer_list
			movie_directors_dict[movie.movieId] = director_list
			movie_actors_dict[movie.movieId] = actor_list
			movie_ratings_dict[movie.movieId] = rating_list


		#self.stdout.write("\nHow similar movies are based on their genres:")
		movie_genres_adj = self.get_adj_dict(movie_genres_dict)
		#self.stdout.write(str(movie_genres_adj))

		#self.stdout.write("\nHow similar movies are based on their writers:")
		movie_writers_adj = self.get_adj_dict(movie_writers_dict)
		#self.stdout.write(str(movie_writers_adj))

		#self.stdout.write("\nHow similar movies are based on their directors:")
		movie_directors_adj = self.get_adj_dict(movie_directors_dict)
		#self.stdout.write(str(movie_directors_adj))

		#self.stdout.write("\nHow similar movies are based on their actors:")
		movie_actors_adj = self.get_adj_dict(movie_actors_dict)
		#self.stdout.write(str(movie_actors_adj))					

		#self.stdout.write("\nHow similar movies are based on user's ratings:")
		movie_ratings_adj = self.get_adj_dict(movie_ratings_dict)
		#self.stdout.write(str(movie_ratings_adj))

		total_movie_adj = {}
		#self.stdout.write("\nTotal Movie Similarity:")
		for movie in all_movies:
			list = []
			for j in range(len(all_movies)):
				actor_val = movie_actors_adj[movie.movieId][j]
				director_val = movie_directors_adj[movie.movieId][j]
				writer_val = movie_writers_adj[movie.movieId][j]
				genre_val = movie_genres_adj[movie.movieId][j]
				rating_val = movie_ratings_adj[movie.movieId][j]
				list += [5/25 * (actor_val + director_val + writer_val + genre_val + rating_val)]
			total_movie_adj[movie.movieId] = list
		#self.stdout.write(str(total_movie_adj))

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

		#self.stdout.write("\nHow similar users are based on their movie ratings:")
		user_ratings_adj = self.get_adj_dict(user_ratings_dict)
		#self.stdout.write(str(user_ratings_adj))

		#self.stdout.write("\nHow similar users are based on their favourite genres:")
		user_genres_adj = self.get_adj_dict(user_genres_dict)
		#self.stdout.write(str(user_genres_adj))

		total_user_adj = {}
		user_ratings_pearsons = {}
		#self.stdout.write("\nTotal User Similarity:")
		for u, user_u in enumerate(all_users):
			list = []
			for j in range(len(all_users)):
				ratings_val = user_ratings_adj[user_u.id][j]
				genres_val = user_genres_adj[user_u.id][j]
				list += [5/10 * (genres_val + ratings_val)]
			total_user_adj[user_u.id] = list

			rlist = []
			for v, user_v in enumerate(all_users):
				#https://study.com/cimages/multimages/16/begning.jpg
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
				#self.stdout.write("Pearsons for " + user_u.username + " vs " + user_v.username + " = " + str(r))
			user_ratings_pearsons[user_u.id] = rlist
		#self.stdout.write(str(total_user_adj))

		#self.stdout.write("\nUser ratings of Movies:")
		#self.stdout.write(str(user_ratings_dict))

		#self.stdout.write("\nMovie ratings per user:")
		#self.stdout.write(str(movie_ratings_dict))
		recommend_dict = {}


		#INSERT RECOMMENDATION ALGORITHM HERE




				




	def get_adj_dict(self, in_dict):
		adj_dict = {}
		for key_i, value_i in in_dict.items():
			list = []
			#self.stdout.write(str(key_i))
			for key_j, value_j in in_dict.items():
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
