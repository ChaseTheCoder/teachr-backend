from rest_framework import serializers
from user_profile.models import UserProfile
from .models import SchoolClass, SchoolDayClass, SchoolYear, SchoolDay

class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = '__all__'

class SchoolDayWithClassesSerializer(serializers.ModelSerializer):
    classes = serializers.SerializerMethodField()

    class Meta:
        model = SchoolDay
        fields = '__all__'

    def get_classes(self, obj):
        classes = SchoolDayClass.objects.filter(school_day=obj)
        return [
            {
                "id": school_day_class.id,
                "school_class_title": school_day_class.school_class.title,
                **SchoolDayClassSerializer(school_day_class).data
            }
            for school_day_class in classes
        ]

class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = '__all__'

class SchoolDayClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolDayClass
        fields = '__all__'

class SchoolDaySerializer(serializers.ModelSerializer):
    school_day_classes = SchoolDayClassSerializer(many=True, read_only=True)

    class Meta:
        model = SchoolDay
        fields = '__all__'