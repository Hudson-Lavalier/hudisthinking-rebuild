from django.shortcuts import render, get_object_or_404
from .models import Project

def project_list(request):
    p_type = request.GET.get('type', '').strip()
    projects = Project.objects.filter(is_published=True)
    if p_type:
        projects = projects.filter(project_type=p_type)
    return render(request, 'projects/list.html', {
        'projects': projects,
        'current_type': p_type,
        'project_types': Project.PROJECT_TYPES,
    })

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return render(request, 'projects/detail.html', {
        'project': project,
    })
