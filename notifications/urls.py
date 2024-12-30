from django.urls import path
from .views import NotificationList, NotificationDetail, UnreadNotificationsCount

urlpatterns = [
  path('notifications/user/<str:user_id>/', NotificationList.as_view(), name='notification-list'),
  path('unread_notification_count/user/<str:user_id>/', UnreadNotificationsCount.as_view(), name='unread-notification-list'),
  path('notification/<str:notification_id>/', NotificationDetail.as_view(), name='notification-detail'),
]