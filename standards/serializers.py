from rest_framework import serializers
from .models import GradeLevels, IssuingAuthority, Subject, Domain, Standard

class IssuingAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuingAuthority
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'title', 'code')

class GradeLevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeLevels
        fields = '__all__'

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = '__all__'