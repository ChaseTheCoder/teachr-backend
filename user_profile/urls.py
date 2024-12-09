from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import UserProfileGetPost, UserProfilePicPatch, UserProfileUpdate, UserProfileBatchList


urlpatterns = [
    path('profile_auth0/<str:auth0_id>', UserProfileGetPost.as_view(), name='user_profile_get_post'),
    path('profile/<str:id>', UserProfileUpdate.as_view(), name='user_profile_update'),
    path('profile_pic/<str:id>', UserProfilePicPatch.as_view(), name='user_profile_update'),
    path('profile_batch/', UserProfileBatchList.as_view(), name='user_profile_update'),
]

urlpatterns_str = str(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)