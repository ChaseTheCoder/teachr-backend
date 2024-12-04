import uuid
from django.db import models

from grade_levels.models import GradeLevel

class Subject(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user_id = models.CharField(max_length=250)
  subject = models.CharField(max_length=250, blank=True, default='')
  grade = models.CharField(max_length=50, blank=True, default='')
  grade_levels = models.ManyToManyField(GradeLevel, related_name='subjects', blank=True)

  # defines whatis displayed on admin
  def __str__(self):
    return self.grade + ', ' + self.subject
  
# UNIT PLAN
class UnitPlan(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user_id = models.CharField(max_length=250)
  title = models.CharField(max_length=100, blank=True, default='')
  overview = models.CharField(max_length=200, blank=True, default='')
  standard = models.TextField(max_length=1000, blank=True, default='')
  subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE, blank=True, default='')

  def __str__(self):
    return self.title

# LESSON PLAN
class LessonPlan(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user_id = models.CharField(max_length=250)
  title = models.CharField(max_length=100, blank=True, default='')
  standard = models.TextField(max_length=1000, blank=True, default='')
  objective = models.TextField(max_length=1000, blank=True, default='')
  body = models.TextField(blank=True, default='')
  unit_plan = models.ForeignKey(UnitPlan, related_name='lessons',on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title