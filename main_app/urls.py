from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    

    path('albums/', views.album_index, name='album-index'),
    path('albums/create/', views.AlbumCreate.as_view(), name='album-create'),
    path('albums/<int:album_id>/', views.album_detail, name='album-detail'),
    path('albums/<int:pk>/update/', views.AlbumUpdate.as_view(), name='album-update'),
    path('albums/<int:pk>/delete/', views.AlbumDelete.as_view(), name='album-delete'),
    path('albums/<int:album_id>/add-listening/', views.add_listening, name='add-listening'),
    path('albums/<int:album_id>/associate-tag/<int:tag_id>/', views.associate_tag, name='associate-tag'),
    path('albums/<int:album_id>/remove-tag/<int:tag_id>/', views.remove_tag, name='remove-tag'),

    path('tags/', views.TagList.as_view(), name='tag-index'),
    path('tags/create/', views.TagCreate.as_view(), name='tag-create'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
    path('tags/<int:pk>/update/', views.TagUpdate.as_view(), name='tag-update'),
    path('tags/<int:pk>/delete/', views.TagDelete.as_view(), name='tag-delete'),
]