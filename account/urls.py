from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="account/logout.html"), name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^register/$', views.register, name="register"),
    path('genre/', views.genrePick, name='genreselect'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),name='password_reset_complete'),
]