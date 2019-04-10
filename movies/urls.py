from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/<int:page_no>/', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('popular/', views.popular, name='popular'),
    path('hotorders/', views.popular_orders, name='popular_orders'),
    path('hotorders/<int:page_no>/', views.popular_orders, name='popular_orders'),
    path('hotratings/', views.popular_ratings, name='popular_ratings'),
    path('hotratings/<int:page_no>/', views.popular_ratings, name='popular_ratings'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre'),
    path('genre/<int:genre_id>/<int:page_no>/', views.genre_detail, name='genre'),
    path('actor/<int:actor_id>/', views.actor_detail, name='actor'),
    path('actor/<int:actor_id>/<int:page_no>/', views.actor_detail, name='actor'),
    path('director/<int:director_id>/', views.director_detail, name='director'),
    path('director/<int:director_id>/<page_no>/', views.director_detail, name='director'),
    path('writer/<int:writer_id>/', views.writer_detail, name='writer'),
    path('writer/<int:writer_id>/<page_no>/', views.writer_detail, name='writer'),
]
