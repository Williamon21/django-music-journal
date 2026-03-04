from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('albums/', views.album_index, name='album-index'),
    path('albums/<int:album_id>/', views.album_detail, name='album-detail'),
]