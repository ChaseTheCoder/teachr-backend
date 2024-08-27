from django import forms
from rest_framework import serializers
from .models import Subject, Resource, UnitPlan, LessonPlan, Material

class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Resource
    fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
  class Meta:
    model = Material
    fields = '__all__'

# LESSON

class LessonPlanDetailSerializer(serializers.ModelSerializer):
  materials = MaterialSerializer(many=True)

  class Meta:
    model = LessonPlan
    fields = '__all__'

class LessonPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonPlan
    fields = ('id', 'title', 'standard', 'objective')

# UNIT

class LessonPlanTitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonPlan
    fields = ('id', 'user_id', 'title')

class UnitPlanPageSerializer(serializers.ModelSerializer):
  lessons = LessonPlanTitleSerializer(many=True)
  resources = ResourceSerializer(many=True)
  class Meta:
    model = UnitPlan
    fields = ('id', 'user_id', 'title', 'overview', 'standard', 'lessons', 'resources')

class UnitPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = ('id', 'user_id', 'title', 'overview', 'standard', 'subject')

# SUBJECT

class UnitPlanTitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = ('id', 'user_id', 'title', 'overview')

class SubjectPageSerializer(serializers.ModelSerializer):
  units = UnitPlanTitleSerializer(many=True)

  class Meta:
    model = Subject
    fields = ('id', 'user_id', 'subject', 'grade', 'units')

class SubjectSerializer(serializers.ModelSerializer):

  class Meta:
    model = Subject
    fields = ('id', 'user_id', 'subject', 'grade')

