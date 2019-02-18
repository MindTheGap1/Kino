from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from account import views

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),
    url(r'^profile/$', TemplateView.as_view(template_name="profile.html"), name='profile'),
    url(r'^signup/$', views.signup.as_view(), name="signup"),
]