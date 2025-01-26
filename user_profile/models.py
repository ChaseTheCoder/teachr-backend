import uuid
from django.db import models

class UserProfile(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  auth0_id = models.CharField(max_length=100, unique=True)
  first_name = models.CharField(max_length=100, blank=True, default='')
  last_name = models.CharField(max_length=100, blank=True, default='')
  teacher_name = models.CharField(max_length=110, blank=True, default='')
  title = models.CharField(max_length=50, blank=True, default='')
  profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
  verified = models.BooleanField(default=False)
  email_domain = models.CharField(max_length=254, blank=True, default='')
  verified_email = models.EmailField(max_length=254, blank=True, default='')