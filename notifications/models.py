import uuid
from django.db import models
from user_profile.models import UserProfile

NOTIFICATION_TYPES = [
    ('comment', 'Comment'),
    ('upvote', 'Upvote'),
    ('upvote_post', 'Upvote_post'),
    ('upvote_comment', 'Upvote_comment'),
]

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    initiator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=36, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    url_id = models.CharField(max_length=36, null=True, blank=True)
    sub_url_id = models.CharField(max_length=36, null=True, blank=True)