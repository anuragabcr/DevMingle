from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag
from .forms import ProjectForm


def projects(request):
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
    tags = Tag.objects.filter(name__icontains=search)
    data = Project.objects.distinct().filter(Q(title__icontains=search) | Q(tags__in=tags))

    page = request.GET.get('page')
    results = 6
    paginator = Paginator(data, results)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'projects/projects.html',
                  {'projects': data, 'search': search, 'paginator': paginator})


def project(request, pk):
    data = Project.objects.get(id=pk)
    tags = data.tags.all()
    return render(request, 'projects/project.html', {'project': data, 'tags': tags})


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            projectData = form.save(commit=False)
            projectData.owner = profile
            projectData.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    data = profile.project_set.get(id=pk)
    form = ProjectForm(instance=data)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    data = profile.project_set.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('projects')
    return render(request, 'projects/delete_object.html', {'object': data})
