from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile, Skill


def profile(request, pk):
    data = Profile.objects.get(id=pk)
    return render(request, 'users/profile.html', {'profile': data})


def profiles(request):
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
    skills = Skill.objects.filter(name__icontains=search)
    data = Profile.objects.distinct().filter(Q(name__icontains=search) | Q(skill__in=skills))

    page = request.GET.get('page')
    results = 6
    paginator = Paginator(data, results)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'users/profiles.html',
                  {'profiles': data, 'search': search, 'paginator': paginator})


@login_required(login_url='login')
def account(request):
    return render(request, 'users/account.html', {'profile': request.user.profile})


@login_required(login_url='login')
def updateAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('account')
        else:
            messages.error(request, form.errors or 'Error occurred during update')

    return render(request, 'users/profile_form.html', {'form': form})


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


@login_required(login_url='login')
def createSkill(request):
    profileData = request.user.profile


    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profileData
            skill.save()

            messages.success(request, 'Skill added!')
            return redirect('account')
        else:
            messages.error(request, form.errors or 'Error occurred during skill ')

    return render(request, 'users/skill_form.html', {'form': SkillForm(), 'type': 'Create'})


@login_required(login_url='login')
def updateSkill(request, pk):
    profileData = request.user.profile
    skill = profileData.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()

            messages.success(request, 'Skill Updated!')
            return redirect('account')
        else:
            messages.error(request, form.errors or 'Error occurred during skill ')

    return render(request, 'users/skill_form.html', {'form': form, 'type': 'Update'})


@login_required(login_url='login')
def deleteSkill(request, pk):
    profileData = request.user.profile
    skill = profileData.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill Deleted successfully')
        return redirect('account')
    return render(request, 'users/delete_skill.html', {'object': skill})
