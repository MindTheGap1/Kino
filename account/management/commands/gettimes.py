from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User as Auth_User
from django.core.management import call_command
from io import StringIO

class Command(BaseCommand):
	help = 'Time how long it takes to run recommendation algorithm for specified users.'

	def add_arguments(self, parser):
		parser.add_argument('-u', '--user', dest='users', type=int, help = 'Indicates how many users to test, leave blank to do all users')

	def handle(self, *args, **options):
		total_time = 0

		if options['users']:
			user_list = Auth_User.objects.all().values_list('id', flat=True)[0:options['users']]
		else:
			user_list = []
		time = []
		for i in range(20):
			out = StringIO()
			if user_list:
				call_command('getrecommends', user_id=user_list, stdout=out)
				#print(out.getvalue())
				#time += [out.getvalue()]
			else:
				call_command('getrecommends', stdout=out)
				#print(out.getvalue())
				#time += [float(out.getvalue())]
			#total_time += time[i]
		#print(time)
		#avg_time = mean(time)
		#print("%s" % avg_time)
		#print("%s" % total_time)