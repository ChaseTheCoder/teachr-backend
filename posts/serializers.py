from rest_framework import serializers

from groups.serializers import GroupPostSerializer
from .models import Grade, Tag, Post, Comment

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag']

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'grade']

class PostSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    has_upvoted = serializers.SerializerMethodField()
    has_downvoted = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    grades = GradeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    group = GroupPostSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'body', 'timestamp', 'upvotes', 'downvotes', 'has_upvoted', 'has_downvoted', 'comments', 'grades', 'tags', 'group', 'public']

    def get_upvotes(self, obj):
        return obj.upvotes.count()

    def get_downvotes(self, obj):
        return obj.downvotes.count()

    def get_has_upvoted(self, obj):
        user_id = self.context.get('request').query_params.get('user_id') if self.context.get('request') else None
        if user_id:
            return obj.upvotes.filter(id=user_id).exists()
        return None

    def get_has_downvoted(self, obj):
        user_id = self.context.get('request').query_params.get('user_id') if self.context.get('request') else None
        if user_id:
            return obj.downvotes.filter(id=user_id).exists()
        return None
    
    def get_comments(self, obj):
        return obj.comments.count()

class CommentSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    has_upvoted = serializers.SerializerMethodField()
    has_downvoted = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'body', 'timestamp', 'upvotes', 'downvotes', 'has_upvoted', 'has_downvoted']

    def get_upvotes(self, obj):
        return obj.upvotes.count()

    def get_downvotes(self, obj):
        return obj.downvotes.count()
    
    def get_has_upvoted(self, obj):
        user_id = self.context.get('request').query_params.get('user_id') if self.context.get('request') else None
        if user_id:
            return obj.upvotes.filter(id=user_id).exists()
        return None

    def get_has_downvoted(self, obj):
        user_id = self.context.get('request').query_params.get('user_id') if self.context.get('request') else None
        if user_id:
            return obj.downvotes.filter(id=user_id).exists()
        return None