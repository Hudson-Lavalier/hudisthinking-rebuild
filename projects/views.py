from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectCategory

def project_list(request):
    type_slug = request.GET.get('type', '').strip()
    categories = ProjectCategory.objects.all().order_by('order', 'name')
    projects = Project.objects.filter(is_published=True).select_related('project_type')
    if type_slug:
        projects = projects.filter(project_type__slug=type_slug)
    return render(request, 'projects/list.html', {
        'projects': projects,
        'current_type': type_slug,
        'project_types': categories,
    })

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return render(request, 'projects/detail.html', {
        'project': project,
    })
