from rest_framework import serializers
from .models import Plan, Resource, UnitPlan, LessonPlan

class PlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = Plan
    fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Resource
    fields = '__all__'

class UnitPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = '__all__'

class LessonPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonPlan
    fields = '__all__'