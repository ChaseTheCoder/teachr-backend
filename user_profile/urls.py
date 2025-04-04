from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import ProfileImageUpload, UserProfileGetPost, UserProfilePicPatch, UserProfileUpdate, UserProfileBatchList, VerifyProfile, UserProfileList


urlpatterns = [
    path('profile_auth0/<str:auth0_id>', UserProfileGetPost.as_view(), name='user_profile_get_post'),
    path('profile/<str:id>', UserProfileUpdate.as_view(), name='user_profile_update'),
    path('profile_pic/<str:id>', UserProfilePicPatch.as_view(), name='user_profile_update'),
    path('profile_batch/', UserProfileBatchList.as_view(), name='user_profile_update'),
    path('verify/<str:id>', VerifyProfile.as_view(), name='verify_email'),
    path('profile/<str:id>/image/', ProfileImageUpload.as_view(), name='profile-image-upload'),
    path('admin/profiles/', UserProfileList.as_view(), name='user_profile_list'),
]

urlpatterns_str = str(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)