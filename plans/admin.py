from django.contrib import admin
from .models import Subject, UnitPlan, LessonPlan

admin.site.register(Subject)
admin.site.register(UnitPlan)
admin.site.register(LessonPlan)