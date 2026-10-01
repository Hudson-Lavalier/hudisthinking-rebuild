import os
from pathlib import Path
from django.contrib import admin
from django import forms
from django.conf import settings
from django.utils.html import format_html
from .models import SiteConfiguration, DBTemplate, NavigationItem, CustomPage, AboutPage, MediaItem

class DBTemplateForm(forms.ModelForm):
    class Meta:
        model = DBTemplate
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 28,
                'style': 'font-family: Consolas, "Courier New", monospace; font-size: 13px; background-color: #121212; color: #00ff66; width: 100%; border: 1px solid #333;'
            })
        }

@admin.register(DBTemplate)
class DBTemplateAdmin(admin.ModelAdmin):
    form = DBTemplateForm
    list_display = ('name', 'description', 'is_active', 'updated_at', 'status_badge')
    list_filter = ('is_active',)
    search_fields = ('name', 'description', 'content')
    fieldsets = (
        ('Template Identification', {
            'fields': ('name', 'description', 'is_active'),
            'description': (
                "Enter template name (e.g. 'base.html', 'home.html', 'about.html', "
                "'philosophy/list.html', 'philosophy/detail.html', 'projects/list.html', 'projects/detail.html'). "
                "When 'is_active' is checked, this database template overrides the filesystem default."
            )
        }),
        ('Template Source Code', {
            'fields': ('content',),
            'description': "Edit raw Django / HTML source code. Changes take effect immediately upon saving."
        }),
    )

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: #00e676; font-weight: bold;">[Active: Overriding Filesystem]</span>')
        return format_html('<span style="color: #888888;">[Inactive: Filesystem Fallback]</span>')
    status_badge.short_description = "Engine Status"

    def save_model(self, request, obj, form, change):
        # If content is empty and template exists on filesystem, prefill from filesystem
        if not obj.content.strip():
            fs_path = Path(settings.BASE_DIR) / 'templates' / obj.name
            if fs_path.exists():
                try:
                    obj.content = fs_path.read_text(encoding='utf-8')
                except Exception:
                    pass
        super().save_model(request, obj, form, change)


class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        widgets = {
            'custom_css': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': '/* e.g., body { font-size: 18px; } */',
                'style': 'font-family: Consolas, monospace; font-size: 13px; background-color: #121212; color: #f5f5f5; width: 100%;'
            }),
            'custom_head_code': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': '<!-- Custom HTML tags or scripts to inject into <head> -->',
                'style': 'font-family: Consolas, monospace; font-size: 13px; background-color: #121212; color: #f5f5f5; width: 100%;'
            }),
        }

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    form = SiteConfigurationForm
    fieldsets = (
        ('Branding & Identity', {
            'fields': ('site_title', 'llc_name', 'tagline', 'logo', 'favicon', 'meta_description'),
            'description': 'Upload your site logo and favicon, and adjust global site identity.'
        }),
        ('Atmospheric Background Firefly Wisps', {
            'fields': ('enable_wisps', 'wisp_count', 'wisp_speed'),
            'description': 'Controls for the subtle floating embers/wisps in the background.'
        }),
        ('Meta-Custom CSS & Styling', {
            'fields': ('custom_css', 'custom_head_code'),
            'description': 'Inject custom CSS rules and head code directly into all live pages.'
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'url', 'location', 'order', 'is_active', 'open_in_new_tab')
    list_editable = ('order', 'is_active')
    list_filter = ('location', 'is_active')
    search_fields = ('label', 'url')


@admin.register(CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'show_featured_image', 'is_published', 'updated_at')
    list_filter = ('is_published', 'show_featured_image')
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Page Content', {
            'fields': ('title', 'slug', 'content', 'is_published')
        }),
        ('Featured Artwork', {
            'fields': ('featured_image', 'show_featured_image'),
            'description': 'Optional visual asset displayed at the top of the page.'
        }),
        ('SEO Metadata', {
            'classes': ('collapse',),
            'fields': ('meta_description',),
        }),
    )


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_featured_image', 'updated_at')
    fieldsets = (
        ('Overview', {
            'fields': ('title', 'content')
        }),
        ('Featured Artwork', {
            'fields': ('featured_image', 'show_featured_image'),
        }),
        ('SEO Metadata', {
            'classes': ('collapse',),
            'fields': ('meta_description',),
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('preview_thumb', 'title', 'media_type', 'file_size_display', 'embed_code', 'uploaded_at')
    list_filter = ('media_type', 'uploaded_at')
    search_fields = ('title', 'description', 'file')
    readonly_fields = ('uploaded_at', 'file_size_display', 'embed_code', 'preview_large')

    fieldsets = (
        ('Upload Asset', {
            'fields': ('title', 'file', 'media_type', 'description')
        }),
        ('Markdown & Asset Details', {
            'fields': ('embed_code', 'file_size_display', 'uploaded_at', 'preview_large'),
            'description': 'Copy and paste the markdown embed code directly into any writing, argument, or page.'
        }),
    )

    def preview_thumb(self, obj):
        if obj.file and obj.media_type == 'image':
            return format_html(
                '<img src="{}" style="height: 38px; width: auto; max-width: 60px; object-fit: contain; border: 1px solid #444; background: #000;" />',
                obj.file.url
            )
        return format_html('<span style="color: #888; font-family: monospace;">[{}]</span>', obj.media_type.upper())
    preview_thumb.short_description = "Preview"

    def preview_large(self, obj):
        if obj.file and obj.media_type == 'image':
            return format_html(
                '<img src="{}" style="max-height: 250px; max-width: 100%; border: 1px solid #444; background: #000;" />',
                obj.file.url
            )
        return "No image preview available."
    preview_large.short_description = "Visual Preview"

    def embed_code(self, obj):
        if not obj.file:
            return "-"
        code = obj.markdown_embed
        return format_html(
            '<input type="text" value="{}" readonly style="width: 100%; max-width: 500px; font-family: monospace; background: #1a1a1a; color: #fff; border: 1px solid #444; padding: 4px 8px;" onclick="this.select();" />',
            code
        )
    embed_code.short_description = "Markdown Embed Code (Click to Copy)"
