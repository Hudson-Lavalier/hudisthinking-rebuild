from django.db import models
from django.urls import reverse
from django.utils import timezone

class Argument(models.Model):
    CATEGORY_CHOICES = [
        ('argument', 'Philosophical Argument'),
        ('essay', 'Essay'),
        ('blog', 'Blog Post'),
        ('fragment', 'Fragment / Note'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly identifier")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='argument')
    thesis = models.CharField(
        max_length=350,
        blank=True,
        help_text="Brief thesis statement or core premise summary"
    )
    content = models.TextField(help_text="Full text (Markdown supported).")
    published_date = models.DateField(default=timezone.now)
    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO & Schema
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Optional SEO description override. If left blank, uses thesis or first sentences."
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords for SEO metadata."
    )

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Philosophical Argument / Writing"
        verbose_name_plural = "Philosophy Archive"

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

    def get_absolute_url(self):
        return reverse('philosophy:detail', kwargs={'slug': self.slug})

    @property
    def estimated_read_time(self):
        words = len(self.content.split())
        minutes = max(1, round(words / 200))
        return f"{minutes} min read"
