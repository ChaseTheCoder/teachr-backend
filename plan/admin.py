from django.contrib import admin
from .models import Plan, Resource, UnitPlan

admin.site.register(Plan)
admin.site.register(Resource)
admin.site.register(UnitPlan)