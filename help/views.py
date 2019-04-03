from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.management import call_command
from django.db.models import Q
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

def help(request):
	template='help\details.html'
	return render(request, template)
