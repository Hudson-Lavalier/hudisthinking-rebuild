from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Project, ProjectCategory

def project_list(request):
    type_slug = request.GET.get('type', '').strip()
    search_query = request.GET.get('q', '').strip()

    categories = ProjectCategory.objects.all().order_by('order', 'name')
    projects = Project.objects.filter(is_published=True).select_related('project_type')

    if type_slug:
        projects = projects.filter(project_type__slug=type_slug)

    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(tagline__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(platform__icontains=search_query) |
            Q(version__icontains=search_query)
        ).distinct()

    return render(request, 'projects/list.html', {
        'projects': projects,
        'current_type': type_slug,
        'search_query': search_query,
        'project_types': categories,
    })

def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related('project_type'),
        slug=slug,
        is_published=True
    )
    return render(request, 'projects/detail.html', {
        'project': project,
    })
