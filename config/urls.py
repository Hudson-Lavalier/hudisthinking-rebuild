from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize Admin portal titles
admin.site.site_header = "HudIsThinking Admin"
admin.site.site_title = "HudIsThinking"
admin.site.index_title = "Archive & Software Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('philosophy/', include('philosophy.urls')),
    path('projects/', include('projects.urls')),
]

# Serve media files in development (Whitenoise serves static in both dev & prod)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
