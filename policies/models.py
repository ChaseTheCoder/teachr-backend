import uuid
from django.db import models

class Policy(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
  type = models.CharField(max_length=50, unique=True)
  content = models.TextField()
  last_updated = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  url_path_name = models.SlugField(max_length=100, unique=True)