from django.contrib import admin
from .models import Plan, Resource, UnitPlan, LessonPlan, LessonOutline, Material

admin.site.register(Plan)
admin.site.register(UnitPlan)
admin.site.register(Resource)
admin.site.register(LessonPlan)
admin.site.register(LessonOutline)
admin.site.register(Material)