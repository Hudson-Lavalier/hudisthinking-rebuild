from django.shortcuts import render, get_object_or_404
from .models import Argument, PhilosophyCategory

def argument_list(request):
    category_slug = request.GET.get('category', '').strip()
    categories = PhilosophyCategory.objects.all().order_by('order', 'name')
    arguments = Argument.objects.filter(is_published=True).select_related('category')
    if category_slug:
        arguments = arguments.filter(category__slug=category_slug)
    return render(request, 'philosophy/list.html', {
        'arguments': arguments,
        'current_category': category_slug,
        'categories': categories,
    })

def argument_detail(request, slug):
    argument = get_object_or_404(Argument, slug=slug, is_published=True)
    return render(request, 'philosophy/detail.html', {
        'argument': argument,
    })
