from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projects.models import Project
from utils import paginate_util
from .forms import ProjectForm, ReviewForm
from .utils import search_projects


def projects(request):
    projects, search_query = search_projects(request)

    custom_range, projects = paginate_util.paginate(request, projects, 6)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    review_form = ReviewForm

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        review = review_form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()
        messages.success(request, 'Review Added')
        project_obj.update_vote_count_ratio
        return redirect('project', pk=project_obj.id)

    context = {
        'project': project_obj,
        'review_form': review_form
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    project_obj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project_obj)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project_obj)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project_obj = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project_obj.delete()
        return redirect('account')

    context = {
        'object': project_obj
    }
    return render(request, 'delete.html', context)
