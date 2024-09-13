from django.db import models
import uuid

class UserProfile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    auth0_user_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    teacher_name = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.user.username