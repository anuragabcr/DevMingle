from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


def projects(request):
    data = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': data})


def project(request, pk):
    data = Project.objects.get(id=pk)
    tags = data.tags.all()
    return render(request, 'projects/project.html', {'project': data, 'tags': tags})
