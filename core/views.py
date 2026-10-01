from django.shortcuts import render, get_object_or_404
from .models import AboutPage, ConnectPage, CustomPage
from philosophy.models import Argument
from projects.models import Project

def home(request):
    recent_arguments = Argument.objects.filter(is_published=True)[:4]
    recent_projects = Project.objects.filter(is_published=True)[:3]
    return render(request, 'home.html', {
        'recent_arguments': recent_arguments,
        'recent_projects': recent_projects,
    })

def about(request):
    about_obj = AboutPage.get_solo()
    return render(request, 'about.html', {
        'about': about_obj,
    })

def connect(request):
    connect_page = ConnectPage.get_solo()
    return render(request, 'connect.html', {
        'connect': connect_page,
    })

def custom_page(request, slug):
    page = get_object_or_404(CustomPage, slug=slug, is_published=True)
    return render(request, 'custom_page.html', {
        'page': page,
    })
