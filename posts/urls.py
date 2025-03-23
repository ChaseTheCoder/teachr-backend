from django.urls import path
from .views import DeleteComment, GradeList, PostByUser, PostDetail, PostFeed, CommentList, PostHomePage, SearchPosts, SearchPostsByGradesAndTags, TagList, TagGetOrCreate, TagSearch, UpdateCommentVote, UpdatePostVote

urlpatterns = [
    path('grades/', GradeList.as_view(), name='grade-list'),
    path('tags/', TagList.as_view(), name='tag-list'),
    path('tag/get/', TagGetOrCreate.as_view(), name='tag-search'),
    path('tags/search/', TagSearch.as_view(), name='tag-search'),
    path('posts/feed/', PostFeed.as_view(), name='post-feed'),
    path('post/<str:post_id>/', PostDetail.as_view(), name='post-detail'),
    path('posts/user/<str:user_id>/', PostByUser.as_view(), name='posts-by-user'),
    path('post/<uuid:post_id>/comments/', CommentList.as_view(), name='comment-list'),
    path('posts/search/', SearchPosts.as_view(), name='search'),
    path('post/<str:post_id>/vote/', UpdatePostVote.as_view(), name='post-vote'),
    path('posts/home_page/', PostHomePage.as_view(), name='post-home-page'),
    path('comment/<str:comment_id>/', DeleteComment.as_view(), name='delete-comment'),
    path('comment/<str:comment_id>/vote/', UpdateCommentVote.as_view(), name='comment-vote'),
    path('posts/search/grades/tags/', SearchPostsByGradesAndTags.as_view(), name='search-posts-by-grades-tags'),
]