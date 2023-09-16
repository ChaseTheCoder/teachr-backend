from django.db import models

class Plan(models.Model):
  subject = models.CharField(max_length=250)
  grade = models.CharField(max_length=50)
  created = models.DateField(auto_now_add=True)

  # defines whatis displayed on admin
  def __str__(self):
    return self.grade + ', ' + self.subject