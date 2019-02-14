from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name='logout'),
    path('profile/', TemplateView.as_view(template_name="account/profile.html"), name='profile'),
    path('signup/', views.signup, name='signup'),
    path('genre/', views.genrePick, name='genreselect'),
]