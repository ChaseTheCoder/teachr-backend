import uuid
from django.db import models
from user_profile.models import UserProfile

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
