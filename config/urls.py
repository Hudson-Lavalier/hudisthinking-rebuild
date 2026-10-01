from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

# Customize Admin portal titles
admin.site.site_header = "HudIsThinking Admin"
admin.site.site_title = "HudIsThinking"
admin.site.index_title = "Archive & Software Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('philosophy/', include('philosophy.urls')),
    path('projects/', include('projects.urls')),
    path('', include('core.urls')),
    # Serve media files (game downloads, uploads) in both dev and production
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
