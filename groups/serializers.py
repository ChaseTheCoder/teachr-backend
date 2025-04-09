from rest_framework import serializers
from .models import Group
from user_profile.serializers import BasicUserProfileSerializer

class GroupListSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_pending = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'title', 'about', 'created_at', 'is_public', 
                'member_count', 'is_member', 'is_admin', 'is_pending']
        read_only_fields = ['id', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_is_member(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            return obj.members.filter(id=user_id).exists()
        return False

    def get_is_admin(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            return obj.admins.filter(id=user_id).exists()
        return False
    
    def get_is_pending(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            return obj.pending_members.filter(id=user_id).exists()
        return False

class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    admins = BasicUserProfileSerializer(many=True, read_only=True)
    is_member = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_pending = serializers.SerializerMethodField()
    profile_pic_url = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'title', 'about', 'created_at', 'is_public', 
                'member_count', 'admins', 'is_member', 
                'is_admin', 'is_pending', 'profile_pic', 'profile_pic_url', 'rules']
        read_only_fields = ['id', 'created_at', 'admins']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_is_member(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            return obj.members.filter(id=user_id).exists()
        return False

    def get_is_admin(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            return obj.admins.filter(id=user_id).exists()
        return False
    
    def get_is_pending(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            return obj.pending_members.filter(id=user_id).exists()
        return False

    def get_profile_pic_url(self, obj):
        if obj.profile_pic:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_pic.url)
        return None
    
class GroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title']

class GroupRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'rules']
        read_only_fields = ['id']