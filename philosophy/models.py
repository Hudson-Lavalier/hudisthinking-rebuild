from django.db import models
from django.urls import reverse
from django.utils import timezone

class PhilosophyCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Category name (e.g. 'Arguments', 'Essays', 'Metaphysics')")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL-friendly identifier")
    description = models.TextField(blank=True, help_text="Short description of this category")
    order = models.PositiveIntegerField(default=0, help_text="Sort order on archive tabs")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Philosophy Category"
        verbose_name_plural = "Philosophy Categories"

    def __str__(self):
        return self.name


class PhilosophyTag(models.Model):
    name = models.CharField(max_length=80, unique=True, help_text="Tag name (e.g. Ethics, Meta-Ethics, Metaphysics, Free Will)")
    slug = models.SlugField(max_length=80, unique=True, help_text="URL-friendly identifier")
    description = models.TextField(blank=True, help_text="Short description of the philosophical domain")

    class Meta:
        ordering = ['name']
        verbose_name = "Philosophy Tag"
        verbose_name_plural = "Philosophy Tags"

    def __str__(self):
        return self.name


class Argument(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-friendly identifier")
    category = models.ForeignKey(
        PhilosophyCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='arguments',
        help_text="Choose or create categories under Philosophy Categories"
    )
    tags = models.ManyToManyField(
        PhilosophyTag,
        blank=True,
        related_name='arguments',
        help_text="Select or create tags such as Ethics, Meta-Ethics, Metaphysics, Free Will"
    )
    thesis = models.CharField(
        max_length=350,
        blank=True,
        help_text="Brief thesis statement or core premise summary"
    )
    content = models.TextField(help_text="Full text (Markdown supported).")
    published_date = models.DateField(default=timezone.now)
    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO & Schema
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Optional SEO description override. If left blank, uses thesis or title."
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
        cat_name = self.category.name if self.category else "Uncategorized"
        return f"[{cat_name}] {self.title}"

    def get_absolute_url(self):
        return reverse('philosophy:detail', kwargs={'slug': self.slug})

    @property
    def estimated_read_time(self):
        words = len(self.content.split())
        minutes = max(1, round(words / 200))
        return f"{minutes} min read"
