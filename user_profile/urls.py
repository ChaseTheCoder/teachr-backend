from django.urls import path, include
from .views import UserProfileGetPost, UserProfileUpdate


urlpatterns = [
    path('profile_auth0/<str:auth0_id>', UserProfileGetPost.as_view(), name='user_profile_get_post'),
    path('profile/<str:id>', UserProfileUpdate.as_view(), name='user_profile_update'),
]

urlpatterns_str = str(urlpatterns)