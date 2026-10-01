from django.urls import path
from . import views

app_name = 'philosophy'

urlpatterns = [
    path('', views.argument_list, name='list'),
    path('<slug:slug>/', views.argument_detail, name='detail'),
]
