from django.urls import path
from .views import NotificationList, NotificationDetail

urlpatterns = [
    path('notifications/user/<str:user_id>/', NotificationList.as_view(), name='notification-list'),
    path('notification/<str:notification_id>/', NotificationDetail.as_view(), name='notification-detail'),
]