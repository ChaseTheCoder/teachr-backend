from django.db import models
import uuid

class UserProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    auth0_user_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    teacher_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username