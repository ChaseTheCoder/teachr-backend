from django import forms
from rest_framework import serializers
from .models import Subject, Resource, UnitPlan, LessonPlan, LessonOutline, Material

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

class LessonPlanDetailSerializer(serializers.ModelSerializer):
  materials = MaterialSerializer(many=True)
  lesson_outline = LessonOutlineSerializer(many=True)

  class Meta:
    model = LessonPlan
    fields = ('id', 'title', 'standard', 'objective', 'lesson_outline', 'materials')

class LessonPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonPlan
    fields = ('id', 'title', 'standard', 'objective')

# UNIT

class LessonPlanTitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonPlan
    fields = ('id', 'title')

class UnitPlanPageSerializer(serializers.ModelSerializer):
  lessons = LessonPlanTitleSerializer(many=True)
  resources = ResourceSerializer(many=True)
  class Meta:
    model = UnitPlan
    fields = ('id', 'title', 'overview', 'standard', 'lessons', 'resources')

class UnitPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = ('id', 'title', 'overview', 'standard', 'subject')

# SUBJECT

class UnitPlanTitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = ('id', 'title', 'overview')

class SubjectPageSerializer(serializers.ModelSerializer):
  units = UnitPlanTitleSerializer(many=True)

  class Meta:
    model = Subject
    fields = ('id', 'subject', 'grade', 'units')

class SubjectSerializer(serializers.ModelSerializer):

  class Meta:
    model = Subject
    fields = ('id', 'subject', 'grade')

