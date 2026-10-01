from django.db import models
from django.urls import reverse

class SiteConfiguration(models.Model):
    site_title = models.CharField(max_length=150, default="HudIsThinking")
    llc_name = models.CharField(max_length=150, default="HudIsThinking LLC")
    tagline = models.CharField(
        max_length=300,
        default="Personal archive of philosophical arguments and software works."
    )
    logo = models.ImageField(
        upload_to='branding/',
        blank=True,
        null=True,
        help_text="Custom site logo (defaults to the H.I.T. book icon if empty)."
    )
    favicon = models.ImageField(
        upload_to='branding/',
        blank=True,
        null=True,
        help_text="Custom browser tab icon (.ico or .png)."
    )
    meta_description = models.TextField(
        blank=True,
        default="Personal archive of philosophical arguments and software works.",
        help_text="Global SEO meta description."
    )
    
    # Atmospheric Firefly Wisps Controls
    enable_wisps = models.BooleanField(
        default=True,
        help_text="Toggle the floating background firefly wisps."
    )
    wisp_count = models.PositiveIntegerField(
        default=16,
        help_text="Number of floating wisps in background (recommended: 10-25)."
    )
    wisp_speed = models.FloatField(
        default=0.08,
        help_text="Drift speed multiplier (recommended: 0.04 to 0.15)."
    )

    # Meta-Custom Styling & Code
    custom_css = models.TextField(
        blank=True,
        help_text="Raw CSS injected into all pages. Use this to tweak colors, fonts, or borders directly from admin."
    )
    custom_head_code = models.TextField(
        blank=True,
        help_text="Custom HTML/scripts to inject into <head> (e.g., custom analytics or font tags)."
    )

    class Meta:
        verbose_name = "Site Configuration & Branding"
        verbose_name_plural = "Site Configuration & Branding"

    def __str__(self):
        return f"{self.site_title} Configuration"

    @classmethod
    def get_solo(cls):
        config, _ = cls.objects.get_or_create(id=1)
        return config


class DBTemplate(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Template path to override (e.g. 'base.html', 'home.html', 'about.html', 'philosophy/list.html', 'philosophy/detail.html', 'projects/list.html', 'projects/detail.html')"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Brief note describing what this template is used for."
    )
    content = models.TextField(
        help_text="HTML / Django template source code. Edit directly in your browser."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="When checked, this database template overrides the filesystem template. Uncheck to revert to default."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Editable Template (DB)"
        verbose_name_plural = "Editable Templates (DB)"

    def __str__(self):
        status = "Active" if self.is_active else "Inactive (Using Default)"
        return f"{self.name} [{status}]"


class NavigationItem(models.Model):
    LOCATION_CHOICES = [
        ('header', 'Header Navigation'),
        ('footer', 'Footer Links'),
    ]

    label = models.CharField(max_length=80, help_text="Display label (e.g., 'Philosophy', 'Projects')")
    url = models.CharField(max_length=255, help_text="URL path (e.g. '/philosophy/', '/projects/', '/about/', or full 'https://...')")
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='header')
    order = models.PositiveIntegerField(default=0, help_text="Order in navigation bar (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ['location', 'order', 'label']
        verbose_name = "Navigation Menu Link"
        verbose_name_plural = "Navigation Menu Links"

    def __str__(self):
        return f"[{self.get_location_display()}] {self.label} -> {self.url}"


class CustomPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="URL slug (e.g. 'manifesto' makes it accessible at /manifesto/)")
    content = models.TextField(help_text="Page body content (Markdown and HTML supported).")
    meta_description = models.CharField(max_length=160, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Custom Standalone Page"
        verbose_name_plural = "Custom Standalone Pages"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:custom_page', kwargs={'slug': self.slug})


class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About HudIsThinking LLC")
    content = models.TextField(
        blank=True,
        help_text="Markdown supported. Leave blank or edit anytime via Django admin."
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO description for search engines."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return self.title
