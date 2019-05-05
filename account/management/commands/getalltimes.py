from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User as Auth_User
from django.core.management import call_command
from movies.models import Movie

class Command(BaseCommand):
	help = 'Time how long it takes to run recommendation algorithm for specified users.'

	def handle(self, *args, **options):
		n = len(Auth_User.objects.all())
		m = len(Movie.objects.all())
		print(str(n) + " users")
		print(str(m) + " movies\n")
		for i in range(n):
			print("/// Times for " + str(i+1) + " user ///")
			call_command('gettimes', users=(i+1))