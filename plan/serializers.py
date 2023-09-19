from rest_framework import serializers
from .models import Plan, Resource, UnitPlan

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