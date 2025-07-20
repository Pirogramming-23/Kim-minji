from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('like/', views.like_post, name='like_post'),
    path('comment/add/', views.add_comment, name='add_comment'),
    path('comment/delete/', views.delete_comment, name='delete_comment'),
]