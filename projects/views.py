from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm


def projects(request):
    data = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': data})


def project(request, pk):
    data = Project.objects.get(id=pk)
    tags = data.tags.all()
    return render(request, 'projects/project.html', {'project': data, 'tags': tags})


def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def updateProject(request, pk):
    data = Project.objects.get(id=pk)
    form = ProjectForm(instance=data)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def deleteProject(request, pk):
    data = Project.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('projects')
    return render(request, 'projects/delete_object.html', {'object': data})
