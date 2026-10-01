from django.db import models

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
