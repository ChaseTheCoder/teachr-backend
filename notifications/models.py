import uuid
from django.db import models
from user_profile.models import UserProfile

NOTIFICATION_TYPES = [
    ('comment', 'Comment')
]

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    initiator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    url_id = models.CharField(max_length=36, null=True, blank=True)
    sub_url_id = models.CharField(max_length=36, null=True, blank=True)