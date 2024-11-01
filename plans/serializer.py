from django import forms
from rest_framework import serializers
from .models import Subject, UnitPlan, LessonPlan

# LESSON

class LessonPlanDetailSerializer(serializers.ModelSerializer):
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
  class Meta:
    model = UnitPlan
    fields = ('id', 'user_id', 'title', 'overview', 'standard', 'lessons')

class UnitPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = ('id', 'user_id', 'title', 'overview', 'standard', 'subject')

# SUBJECT
class UnitPlanTitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitPlan
    fields = ('id', 'user_id', 'title')

class SubjectPageSerializer(serializers.ModelSerializer):
  units = UnitPlanTitleSerializer(many=True)

  class Meta:
    model = Subject
    fields = ('id', 'user_id', 'subject', 'grade', 'grade_levels', 'units')

class SubjectSerializer(serializers.ModelSerializer):

  class Meta:
    model = Subject
    fields = ('id', 'user_id', 'subject', 'grade', 'grade_levels')



class PlanUnitTitleSerializer(serializers.ModelSerializer):
  lessons = LessonPlanTitleSerializer(many=True)
  class Meta:
    model = UnitPlan
    fields = ('id', 'user_id', 'title', 'lessons')

class PlansSerializer(serializers.ModelSerializer):
  units = PlanUnitTitleSerializer(many=True)
  class Meta:
    model = Subject
    fields = ('id', 'user_id', 'subject', 'grade', 'grade_levels', 'units')

