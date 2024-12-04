from django.urls import path
from .views import PostByUser, PostDetail, PostFeed, CommentList

urlpatterns = [
    path('posts/feed/', PostFeed.as_view(), name='post-feed'),
    path('post/<str:post_id>/', PostDetail.as_view(), name='post-detail'),
    path('posts/user/<str:user_id>/', PostByUser.as_view(), name='posts-by-user'),
    path('post/<uuid:post_id>/comments/', CommentList.as_view(), name='comment-list'),
]