from django.urls import path
from . import views, api_views

app_name = 'core'

urlpatterns = [
    # In-Situ Live Editor API Endpoints
    path('api/live-editor/save/', api_views.live_save, name='api_live_save'),
    path('api/live-editor/media/', api_views.live_media_list, name='api_live_media'),

    path('', views.home, name='home'),
    path('connect/', views.connect, name='connect'),
    path('about/', views.about, name='about'),
    path('page/<slug:slug>/', views.custom_page, name='custom_page'),
    path('<slug:slug>/', views.custom_page, name='custom_page_direct'),
]
