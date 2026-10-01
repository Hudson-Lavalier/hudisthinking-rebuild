from django.contrib import admin
from .models import Project, ProjectCategory

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'version', 'platform', 'release_date', 'is_published')
    list_filter = ('project_type', 'platform', 'is_published', 'release_date')
    search_fields = ('title', 'tagline', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Overview', {
            'fields': ('title', 'slug', 'project_type', 'tagline', 'description', 'release_date', 'is_published')
        }),
        ('Downloadable Binary / Executable', {
            'fields': ('download_file', 'version', 'platform', 'system_requirements'),
            'description': 'Attach your packaged .exe or .zip archive here.'
        }),
        ('External Links', {
            'fields': ('github_url', 'itch_url'),
        }),
        ('SEO Metadata (Optional)', {
            'classes': ('collapse',),
            'fields': ('meta_description',),
        }),
    )
