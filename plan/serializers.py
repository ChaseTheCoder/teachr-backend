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

# LESSON

class LessonPlanSerializer(serializers.ModelSerializer):
  # materials = MaterialSerializer(many=True)
  lesson_outline = LessonOutlineSerializer(many=True)

  class Meta:
    model = LessonPlan
    fields = ('id', 'title', 'standard', 'objective', 'lesson_outline')

# UNIT

class LessonPlanTitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonPlan
    fields = ('id', 'title')

class UnitPlanSerializer(serializers.ModelSerializer):
  lessons = LessonPlanTitleSerializer(many=True)
  resources = ResourceSerializer(many=True)
  class Meta:
    model = UnitPlan
    fields = ('id', 'title', 'overview', 'standard', 'lessons', 'resources')

# PLAN

class UnitPlanTitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = ('id', 'title', 'overview')

class PlanSerializer(serializers.ModelSerializer):
  units = UnitPlanTitleSerializer(many=True)

  class Meta:
    model = Plan
    fields = ('id', 'subject', 'grade', 'units')

