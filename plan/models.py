from django.db import models

class Plan(models.Model):
  subject = models.CharField(max_length=250)
  grade = models.CharField(max_length=50)
  created = models.DateField(auto_now_add=True)

  # defines whatis displayed on admin
  def __str__(self):
    return self.grade + ', ' + self.subject
  
class Resource(models.Model):
  link = models.URLField()
  title = models.CharField(max_length=50)

  def __str__(self):
    return self.title
  
class UnitPlan(models.Model):
  title = models.CharField(max_length=100)
  overview = models.CharField(max_length=200)
  standard = models.TextField(max_length=1000)
  resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
  subject = models.ForeignKey(Plan, on_delete=models.CASCADE)