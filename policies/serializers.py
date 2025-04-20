from rest_framework import serializers
from .models import Policy

class PolicyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = ['id', 'type']
        read_only_fields = ['id', 'last_updated', 'created_at']

class PolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = ['type', 'content', 'last_updated', 'created_at', 'url_path_name']
        read_only_fields = ['id', 'last_updated', 'created_at']

class PolicyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'type', 'content', 'last_updated', 'created_at', 'url_path_name']
        read_only_fields = ['id', 'last_updated', 'created_at']