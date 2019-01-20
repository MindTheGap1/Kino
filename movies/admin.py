from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Movies)
admin.site.register(Actors)
admin.site.register(Genres)
admin.site.register(Directors)
admin.site.register(Writers)
admin.site.register(MovieActors)
admin.site.register(MovieGenres)
admin.site.register(MovieDirectors)
admin.site.register(MovieWriters)
