from django.contrib import admin
from .models import Argument, PhilosophyCategory, PhilosophyTag

@admin.register(PhilosophyCategory)
class PhilosophyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(PhilosophyTag)
class PhilosophyTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'argument_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def argument_count(self, obj):
        return obj.arguments.count()
    argument_count.short_description = "Associated Arguments"


@admin.register(Argument)
class ArgumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'tag_list', 'show_featured_image', 'published_date', 'is_published')
    list_filter = ('category', 'tags', 'show_featured_image', 'is_published', 'published_date')
    search_fields = ('title', 'thesis', 'content', 'justifications', 'references')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'category', 'tags', 'thesis', 'content', 'published_date', 'is_published')
        }),
        ('Featured Artwork', {
            'fields': ('featured_image', 'show_featured_image'),
            'description': 'Header artwork displayed at the top of the argument.'
        }),
        ('Philosophical Apparatus (Accordions)', {
            'fields': ('justifications', 'references'),
            'description': 'Breakdown of premise warrants (Justifications/Elaborations) and bibliographic sources (References). Markdown supported.'
        }),
        ('Academic Citation Formats', {
            'classes': ('collapse',),
            'fields': ('citation_apa', 'citation_mla'),
            'description': 'Custom APA/MLA citation strings for readers to cite this work. If left blank, standard citations will be auto-generated.'
        }),
        ('SEO & Metadata (Optional)', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'meta_keywords'),
            'description': 'Search engine optimization fields. Safe to leave blank for auto-generation.'
        }),
    )

    def tag_list(self, obj):
        return ", ".join([t.name for t in obj.tags.all()]) or "-"
    tag_list.short_description = "Tags"
