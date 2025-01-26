from rest_framework import serializers
from .models import SchoolDomain

class SchoolDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolDomain
        fields = '__all__'

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()