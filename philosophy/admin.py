from django.contrib import admin
from .models import Argument, PhilosophyCategory

@admin.register(PhilosophyCategory)
class PhilosophyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Argument)
class ArgumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'is_published')
    list_filter = ('category', 'is_published', 'published_date')
    search_fields = ('title', 'thesis', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'category', 'thesis', 'content', 'published_date', 'is_published')
        }),
        ('SEO & Metadata (Optional)', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'meta_keywords'),
            'description': 'Search engine optimization fields. Safe to leave blank for auto-generation.'
        }),
    )
