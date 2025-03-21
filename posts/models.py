import uuid
from django.db import models
from user_profile.models import UserProfile

class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    grade = models.CharField(max_length=50, unique=True)

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tag = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(UserProfile, related_name='upvoted_posts', default=None, blank=True)
    downvotes = models.ManyToManyField(UserProfile, related_name='downvoted_posts', default=None, blank=True)
    grades = models.ManyToManyField(Grade, related_name='posts', blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(UserProfile, related_name='upvoted_comments', default=None, blank=True)
    downvotes = models.ManyToManyField(UserProfile, related_name='downvoted_comments', default=None, blank=True)