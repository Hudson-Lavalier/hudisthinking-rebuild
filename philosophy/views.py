from django.shortcuts import render, get_object_or_404
from .models import Argument

def argument_list(request):
    category = request.GET.get('category', '').strip()
    arguments = Argument.objects.filter(is_published=True)
    if category:
        arguments = arguments.filter(category=category)
    return render(request, 'philosophy/list.html', {
        'arguments': arguments,
        'current_category': category,
        'categories': Argument.CATEGORY_CHOICES,
    })

def argument_detail(request, slug):
    argument = get_object_or_404(Argument, slug=slug, is_published=True)
    return render(request, 'philosophy/detail.html', {
        'argument': argument,
    })
