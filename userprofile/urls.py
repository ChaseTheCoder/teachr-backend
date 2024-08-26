from django.urls import path
from .views import PostUserProfileDetail, UserProfileDetail

urlpatterns = [
    path('profile/', PostUserProfileDetail.as_view(), name='user-profile'),
    path('profile/<str:auth0_user_id>/', UserProfileDetail.as_view(), name='user-profile-test'),
]