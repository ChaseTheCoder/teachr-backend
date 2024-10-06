import uuid
from django.db import models

class UserProfile(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  auth0_id = models.CharField(max_length=100, unique=True)
  first_name = models.CharField(max_length=100, blank=True, default='')
  last_name = models.CharField(max_length=100, blank=True, default='')
  teacher_name = models.CharField(max_length=110, blank=True, default='')

  def __str__(self):
      return self.user.username