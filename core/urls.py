from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('connect/', views.connect, name='connect'),
    path('about/', views.about, name='about'),
    path('page/<slug:slug>/', views.custom_page, name='custom_page'),
    path('<slug:slug>/', views.custom_page, name='custom_page_direct'),
]
