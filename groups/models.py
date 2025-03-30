import uuid
import os
from django.db import models
from user_profile.models import UserProfile

def group_profile_image_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create filename as UUID
    filename = f"{str(instance.id)}.{ext}"
    return os.path.join('group_pics', filename)

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    members = models.ManyToManyField(UserProfile, related_name='groups')
    pending_members = models.ManyToManyField(UserProfile, related_name='pending_groups', blank=True)
    admins = models.ManyToManyField(UserProfile, related_name='administered_groups')
    profile_pic = models.ImageField(
        upload_to=group_profile_image_path,
        null=True,
        blank=True
    )