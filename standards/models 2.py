import uuid
from django.db import models
from grade_levels.models import GradeLevel

class IssuingAuthority(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255)
  code = models.CharField(max_length=50, null=True, blank=True)

  def __str__(self):
    return self.title

class Subject(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255)
  code = models.CharField(max_length=50, null=True, blank=True)
  issuing_authority = models.ForeignKey(IssuingAuthority, related_name='subjects', on_delete=models.CASCADE)

  def __str__(self):
    return self.title
  
class GradeLevels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    grade_levels = models.ManyToManyField(GradeLevel, related_name='standard_grade_levels')
    subject = models.ForeignKey(Subject, related_name='grade_levels', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Domain(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=500)
  code = models.CharField(max_length=50, null=True, blank=True)
  grade_levels = models.ManyToManyField(GradeLevels, related_name='domains')

  def __str__(self):
    return self.title

class Standard(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=500)
  code = models.CharField(max_length=50, null=True, blank=True)
  full_code = models.CharField(max_length=200)
  domain = models.ForeignKey(Domain, related_name='standards', on_delete=models.CASCADE)
  grade_levels = models.ForeignKey(GradeLevels, related_name='standard', on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.full_standard_code
