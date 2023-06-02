from django.urls import path
from . import views

urlpatterns = [
    path('', views.info_about_arts, name='info_about_arts'),
]