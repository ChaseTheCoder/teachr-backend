from django.urls import path
from .views import PostByUser, PostFeed

urlpatterns = [
    path('posts/feed', PostFeed.as_view(), name='post-feed'),
    path('posts/user/<str:user_id>', PostByUser.as_view(), name='posts-by-user'),
    path('posts/<str:post_id>', PostByUser.as_view(), name='post-detail'),
]