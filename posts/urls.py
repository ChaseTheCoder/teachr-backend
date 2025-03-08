from django.urls import path
from .views import DeleteComment, PostByUser, PostDetail, PostFeed, CommentList, SearchPosts, TagList, TagSearch, UpdateCommentVote, UpdatePostVote

urlpatterns = [
    path('tags/', TagList.as_view(), name='tag-list'),
    path('tag/search/', TagSearch.as_view(), name='tag-search'),
    path('posts/feed/', PostFeed.as_view(), name='post-feed'),
    path('post/<str:post_id>/', PostDetail.as_view(), name='post-detail'),
    path('posts/user/<str:user_id>/', PostByUser.as_view(), name='posts-by-user'),
    path('post/<uuid:post_id>/comments/', CommentList.as_view(), name='comment-list'),
    path('comment/<str:comment_id>/', DeleteComment.as_view(), name='delete-comment'),
    path('posts/search/', SearchPosts.as_view(), name='search'),
    path('post/<str:post_id>/vote/', UpdatePostVote.as_view(), name='post-vote'),
    path('comment/<str:comment_id>/vote/', UpdateCommentVote.as_view(), name='comment-vote'),
]