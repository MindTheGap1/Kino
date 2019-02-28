from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('results/', views.searchMovie, name='search_movie'),
]