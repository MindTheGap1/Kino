from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect


class signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/landing/')
    else:
        template = 'profile.html'
        return render(request, template)