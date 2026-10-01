from django.contrib import admin
from .models import AboutPage

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')

    def has_add_permission(self, request):
        # Only allow one About page record
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
