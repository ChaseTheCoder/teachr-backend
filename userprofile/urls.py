from django.urls import path
from .views import UserProfileDetail

urlpatterns = [
    path('profile/', UserProfileDetail.as_view(), name='user-profile'),
]