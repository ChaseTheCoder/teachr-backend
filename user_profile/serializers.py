from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'created_at', 'auth0_id', 'first_name', 'last_name', 'teacher_name', 'title', 'verified', 'email_domain', 'profile_pic_url')

    def get_profile_pic_url(self, obj):
        if obj.profile_pic:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_pic.url)
        return None

class BasicUserProfileSerializer(serializers.ModelSerializer):
    profile_pic_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ('id', 'teacher_name', 'title', 'verified', 'profile_pic_url')

    def get_profile_pic_url(self, obj):
        if obj.profile_pic:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_pic.url)
        return None