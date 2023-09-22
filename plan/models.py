from django.db import models

class Plan(models.Model):
  subject = models.CharField(max_length=250)
  grade = models.CharField(max_length=50)

  # defines whatis displayed on admin
  def __str__(self):
    return self.grade + ', ' + self.subject
  
# UNIT PLAN
class Resource(models.Model):
  link = models.URLField(default='DEFAULT VALUE')
  title = models.CharField(max_length=50)

  def __str__(self):
    return self.title
  
class UnitPlan(models.Model):
  title = models.CharField(max_length=100)
  overview = models.CharField(max_length=200)
  standard = models.TextField(max_length=1000)
  resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
  subject = models.ForeignKey(Plan, on_delete=models.CASCADE)

  def __str__(self):
    return self.title

# LESSON PLAN

class LessonOutline(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=1000)

class LessonPlan(models.Model):
  title = models.CharField(max_length=100)
  standard = models.TextField(max_length=1000)
  objective = models.TextField(max_length=1000)
  outline = models.ForeignKey(LessonOutline, on_delete=models.CASCADE, null=True, blank=True)
  unitplan = models.ForeignKey(UnitPlan, on_delete=models.CASCADE) # FIX It is impossible to add a non-nullable field 'unitplan' to lessonplan without specifying a default.

  def __str__(self):
    return self.title