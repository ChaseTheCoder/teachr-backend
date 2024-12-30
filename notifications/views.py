from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer

class NotificationList(APIView):
    def get(self, request, user_id, *args, **kwargs):
        notifications = Notification.objects.filter(user=user_id)
        page = int(request.query_params.get('page', 1))
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        notifications = notifications.order_by('-timestamp')[start:end]
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id, *args, **kwargs):
        notifications = Notification.objects.filter(user=user_id, read=False)
        notifications.update(read=True)
        return Response(status=status.HTTP_200_OK)

class UnreadNotificationsCount(APIView):
    def get(self, request, user_id, *args, **kwargs):
        count = Notification.objects.filter(user=user_id, read=False).count()
        return Response({"count": count}, status=status.HTTP_200_OK)

class NotificationDetail(APIView):
    def delete(self, request, notification_id, *args, **kwargs):
        notification = get_object_or_404(Notification, id=notification_id)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, notification_id, *args, **kwargs):
        notification = get_object_or_404(Notification, id=notification_id)
        notification.read = True
        notification.save()
        return Response(status=status.HTTP_200_OK)