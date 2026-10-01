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
    list_display = ('title', 'project_type', 'version', 'show_download_button', 'show_featured_image', 'is_published', 'release_date')
    list_editable = ('show_download_button', 'show_featured_image')
    list_filter = ('project_type', 'show_download_button', 'show_featured_image', 'platform', 'is_published', 'release_date')
    search_fields = ('title', 'tagline', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Overview', {
            'fields': ('title', 'slug', 'project_type', 'tagline', 'description', 'release_date', 'is_published')
        }),
        ('Featured Artwork', {
            'fields': ('featured_image', 'show_featured_image'),
            'description': 'Screenshot, artwork, or user interface preview.'
        }),
        ('Downloadable Binary / Executable', {
            'fields': ('download_file', 'download_url', 'show_download_button', 'version', 'platform', 'system_requirements'),
            'description': 'Upload your packaged executable (.exe, .zip) or enter an external download link. Toggle the download button visibility above.'
        }),
        ('External Links', {
            'fields': ('github_url', 'itch_url'),
        }),
        ('SEO Metadata (Optional)', {
            'classes': ('collapse',),
            'fields': ('meta_description',),
        }),
    )
