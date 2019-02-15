from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre'),
    path('actor/<int:actor_id>/', views.actor_detail, name='actor'),
    path('director/<int:director_id>/', views.director_detail, name='director'),
    path('writer/<int:writer_id>/', views.writer_detail, name='writer'),
]
