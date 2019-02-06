"""Kino URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include,path
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('movies/', include('movies.urls', namespace= 'movies')),
    path('',include('movies.urls'),name ='main'),
    #TODO: Include these in their own account/urls.py file
    url(r'^login/$', auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="account/logout.html"), name='logout'),
    #TODO: Create profile view to dynamically add user profile info
    url(r'^profile/$', TemplateView.as_view(template_name="account/profile.html"), name='profile'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
