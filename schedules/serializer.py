from rest_framework import serializers
from user_profile.models import UserProfile
from .models import SchoolYear, SchoolDay

class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = '__all__'

class SchoolDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolDay
        fields = '__all__'