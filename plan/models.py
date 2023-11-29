from django.db import models

class Plan(models.Model):
  subject = models.CharField(max_length=250)
  grade = models.CharField(max_length=50)

  # defines whatis displayed on admin
  def __str__(self):
    return self.grade + ', ' + self.subject
  
# UNIT PLAN
class UnitPlan(models.Model):
  title = models.CharField(max_length=100)
  overview = models.CharField(max_length=200)
  standard = models.TextField(max_length=1000)
  subject = models.ForeignKey(Plan, related_name='units', on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return self.title

# Resource
class Resource(models.Model):
  link = models.URLField(null=True, blank=True)
  title = models.CharField(max_length=50)
  resource = models.ForeignKey(UnitPlan, related_name='resources', on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title

# LESSON PLAN
class LessonPlan(models.Model):
  title = models.CharField(max_length=100)
  standard = models.TextField(max_length=1000)
  objective = models.TextField(max_length=1000)
  unit_plan = models.ForeignKey(UnitPlan, related_name='lessons',on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title

# LESSON PLAN OUTLINE
class LessonOutline(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=1000)
  lesson_plan = models.ForeignKey(LessonPlan, related_name='lesson_outline', on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title

# Resource
class Material(models.Model):
  title = models.CharField(max_length=50)
  link = models.URLField(null=True, blank=True)
  lesson_plan = models.ForeignKey(LessonPlan, related_name='materials', on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title