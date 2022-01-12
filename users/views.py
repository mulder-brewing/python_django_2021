from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from utils import paginate_util
from .forms import MyUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile
from .utils import search_profiles


# Create your views here.

def profiles(request):
    profiles_obj, search_query = search_profiles(request)
    custom_range, profiles_obj = paginate_util.paginate(request, profiles_obj, 6)

    context = {
        'profiles': profiles_obj,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile_obj = Profile.objects.get(id=pk)

    top_skills = profile_obj.skill_set.exclude(description__exact="")
    other_skills = profile_obj.skill_set.filter(description="")

    context = {
        'profile': profile_obj,
        'top_skills': top_skills,
        'other_skills': other_skills
    }
    return render(request, 'users/user-profile.html', context)


def user_login(request):
    context = {
        'page': 'login'
    }

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password incorrect')

    return render(request, 'users/login_register.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out')
    return redirect('login')


def register_user(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {
        'page': 'register',
        'form': form
    }

    return render(request, 'users/login_register.html', context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'users/account.html', context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/profile_form.html', context)


@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added')
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated')
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted')
        return redirect('account')

    context = {
        'object': skill
    }
    return render(request, 'delete.html', context)


@login_required(login_url="login")
def inbox(request):
    user_messages = request.user.profile.messages.all()
    context = {
        'user_messages': user_messages,
        'unread_count': user_messages.filter(is_read=False).count()
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def message(request, pk):
    user_message = request.user.profile.messages.get(id=pk)

    if not user_message.is_read:
        user_message.is_read = True
        user_message.save()

    context = {
        'user_message': user_message
    }
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    sender = request.user.profile if request.user.is_authenticated else None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()

            messages.success(request, 'Message sent')
            return redirect('user-profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message_form.html', context)
