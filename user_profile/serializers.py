from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'created_at', 'auth0_id', 'first_name', 'last_name', 'teacher_name', 'title', 'verified', 'email_domain')

class BasicUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'teacher_name', 'title', 'verified')