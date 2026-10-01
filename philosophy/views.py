from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Argument, PhilosophyCategory, PhilosophyTag

def argument_list(request):
    category_slug = request.GET.get('category', '').strip()
    tag_slug = request.GET.get('tag', '').strip()
    search_query = request.GET.get('q', '').strip()

    categories = PhilosophyCategory.objects.all().order_by('order', 'name')
    all_tags = PhilosophyTag.objects.all().order_by('name')
    arguments = Argument.objects.filter(is_published=True).select_related('category').prefetch_related('tags')

    if category_slug:
        arguments = arguments.filter(category__slug=category_slug)

    if tag_slug:
        arguments = arguments.filter(tags__slug=tag_slug)

    if search_query:
        arguments = arguments.filter(
            Q(title__icontains=search_query) |
            Q(thesis__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()

    return render(request, 'philosophy/list.html', {
        'arguments': arguments,
        'current_category': category_slug,
        'current_tag': tag_slug,
        'search_query': search_query,
        'categories': categories,
        'all_tags': all_tags,
    })

def argument_detail(request, slug):
    argument = get_object_or_404(
        Argument.objects.prefetch_related('tags').select_related('category'),
        slug=slug,
        is_published=True
    )
    return render(request, 'philosophy/detail.html', {
        'argument': argument,
    })
