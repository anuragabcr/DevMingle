from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
from .forms import CustomUserCreationForm
from .models import Profile


def profile(request, pk):
    data = Profile.objects.get(id=pk)
    return render(request, 'users/profile.html', {'profile': data})


def profiles(request):
    data = Profile.objects.all()
    return render(request, 'users/profiles.html', {'profiles': data})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('projects')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('projects')
        else:
            messages.error(request, 'Incorrect username or password')

    return render(request, 'users/login_register.html', {'page': 'login'})


def logoutPage(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('projects')


def registerPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account created!')

            login(request, user)
            return redirect('projects')
        else:
            messages.error(request, form.errors or 'Error occurred during registration')

    return render(request, 'users/login_register.html', {'page': 'register', 'form': CustomUserCreationForm()})
