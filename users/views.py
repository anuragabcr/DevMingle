from django.shortcuts import render
from .models import Profile


def profile(request, pk):
    data = Profile.objects.get(id=pk)
    return render(request, 'users/profile.html', {'profile': data})


def profiles(request):
    data = Profile.objects.all()
    return render(request, 'users/profiles.html', {'profiles': data})
