from django.contrib import admin
from .models import Subject, Resource, UnitPlan, LessonPlan, Material

admin.site.register(Subject)
admin.site.register(UnitPlan)
admin.site.register(Resource)
admin.site.register(LessonPlan)
admin.site.register(Material)