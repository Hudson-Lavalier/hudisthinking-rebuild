import os
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Project(models.Model):
    PROJECT_TYPES = [
        ('game', 'Game'),
        ('executable', 'Packaged Executable'),
        ('tool', 'Software Tool'),
        ('experiment', 'Experimental Prototype'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly identifier")
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES, default='game')
    tagline = models.CharField(
        max_length=300,
        help_text="One-line summary for listing cards."
    )
    description = models.TextField(
        help_text="Project details, controls, instructions (Markdown supported)."
    )
    download_file = models.FileField(
        upload_to='downloads/',
        blank=True,
        null=True,
        help_text="Upload packaged executable or archive (.exe, .zip, etc.)"
    )
    version = models.CharField(max_length=50, default="1.0.0")
    platform = models.CharField(
        max_length=100,
        default="Windows x64",
        help_text="Target platform (e.g., Windows x64, Cross-platform, Portable)"
    )
    system_requirements = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g., Windows 10/11, Dedicated GPU recommended"
    )
    github_url = models.URLField(blank=True, help_text="Optional GitHub repository link")
    itch_url = models.URLField(blank=True, help_text="Optional Itch.io page link")
    is_published = models.BooleanField(default=True, db_index=True)
    release_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO & Schema
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Optional SEO description override."
    )

    class Meta:
        ordering = ['-release_date', '-created_at']
        verbose_name = "Project / Downloadable Work"
        verbose_name_plural = "Projects & Downloads"

    def __str__(self):
        return f"[{self.get_project_type_display()}] {self.title} ({self.version})"

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    @property
    def file_size_display(self):
        if not self.download_file:
            return None
        try:
            size_bytes = self.download_file.size
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        except Exception:
            return None

    @property
    def filename(self):
        if self.download_file:
            return os.path.basename(self.download_file.name)
        return None
