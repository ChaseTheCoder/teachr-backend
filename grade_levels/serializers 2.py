from rest_framework import serializers
from .models import GradeLevel

class GradeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeLevel
        fields = ('id', 'grade_level')