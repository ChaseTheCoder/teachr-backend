import uuid
from django.db import models

class SchoolYear(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('user_profile.UserProfile', on_delete=models.CASCADE, related_name='school_years')
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

class SchoolClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name='classes')

class SchoolDay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name='days')
    date = models.DateField(unique=True)

class SchoolDayClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_day = models.ForeignKey(SchoolDay, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = [['school_day', 'order'], ['school_day', 'school_class']]