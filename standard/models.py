import uuid
from django.db import models

class EducationStandard(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  education_standard = models.CharField(max_length=100)

  def __str__(self):
    return self.title

class Subject(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  subject = models.CharField(max_length=200)
  standard = models.ForeignKey(EducationStandard, related_name='standards', on_delete=models.CASCADE, blank=False)

  def __str__(self):
    return self.title

class Grade(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  grade = models.CharField(max_length=50)
  subject = models.ForeignKey(Subject, related_name='grades', on_delete=models.CASCADE, blank=False)

  def __str__(self):
    return self.title

class Domain(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  domain = models.CharField(max_length=200, blank=True, default='')
  grade = models.ForeignKey(Grade, related_name='domains', on_delete=models.CASCADE, blank=False)

  def __str__(self):
    return self.title

class Standard(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  standard_code = models.CharField(max_length=10, blank=True, default='')
  grade = models.ForeignKey(Domain, related_name='standards', on_delete=models.CASCADE, blank=False)

  def __str__(self):
    return self.title


