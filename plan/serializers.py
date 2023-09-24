from rest_framework import serializers
from .models import Plan, Resource, UnitPlan, LessonPlan, LessonOutline, Material

class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Resource
    fields = '__all__'

class LessonOutlineSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonOutline
    fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
  class Meta:
    model = Material
    fields = '__all__'

class LessonPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonPlan
    fields = '__all__'

class UnitPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = '__all__'

# PLAN PAGE 
class UnitPlanTitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = 'title'

class PlanSerializer(serializers.ModelSerializer):
  units = UnitPlanSerializer(many=True)

  class Meta:
    model = Plan
    fields = ('subject', 'grade', 'units')

