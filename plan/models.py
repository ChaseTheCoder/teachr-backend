from django.db import models

class Subject(models.Model):
  subject = models.CharField(max_length=250)
  grade = models.CharField(max_length=50)

  # defines whatis displayed on admin
  def __str__(self):
    return self.grade + ', ' + self.subject
  
# UNIT PLAN
class UnitPlan(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')
  overview = models.CharField(max_length=200, blank=True, default='')
  standard = models.TextField(max_length=1000, blank=True, default='')
  subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE, blank=True, default='')

  def __str__(self):
    return self.title

# RESOURCE
class Resource(models.Model):
  link = models.URLField(blank=False, default='')
  title = models.CharField(max_length=50, blank=True, default='')
  unit_plan = models.ForeignKey(UnitPlan, related_name='resources', on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title

# LESSON PLAN
class LessonPlan(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')
  standard = models.TextField(max_length=1000, blank=True, default='')
  objective = models.TextField(max_length=1000, blank=True, default='')
  unit_plan = models.ForeignKey(UnitPlan, related_name='lessons',on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title

# LESSON PLAN OUTLINE
class LessonOutline(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')
  description = models.TextField(max_length=1000, blank=True, default='')
  lesson_plan = models.ForeignKey(LessonPlan, related_name='lesson_outline', on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title

# MATERIAL
class Material(models.Model):
  title = models.CharField(max_length=50)
  link = models.URLField(null=True, blank=True)
  lesson_plan = models.ForeignKey(LessonPlan, related_name='materials', on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.title