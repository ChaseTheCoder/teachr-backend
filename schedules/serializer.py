from rest_framework import serializers
from user_profile.models import UserProfile
from .models import SchoolClass, SchoolDayClass, SchoolYear, SchoolDay

class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = '__all__'

class SchoolDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolDay
        fields = '__all__'

class SchoolDayWithClassesSerializer(serializers.ModelSerializer):
    classes = serializers.SerializerMethodField()

    class Meta:
        model = SchoolDay
        fields = '__all__'

    def get_classes(self, obj):
        classes = SchoolDayClass.objects.filter(school_day=obj)
        return SchoolDayClassSerializer(classes, many=True).data

class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = '__all__'

class SchoolDayClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolDayClass
        fields = '__all__'

