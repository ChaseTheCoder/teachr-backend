from rest_framework import serializers
from .models import Policy

class PolicyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'type', 'url_path_name']
        read_only_fields = ['id', 'type', 'url_path_name']

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['type', 'content', 'last_updated', 'created_at', 'url_path_name']
        read_only_fields = ['type', 'content', 'last_updated', 'created_at', 'url_path_name']

class PolicyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'type', 'content', 'last_updated', 'created_at', 'url_path_name']