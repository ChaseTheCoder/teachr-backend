from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from notifications.models import Notification
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostByUser(APIView):
    def get(self, request, user_id, *args, **kwargs):
        posts = Post.objects.filter(user=user_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, *args, **kwargs):
        data = request.data.copy()
        data['user'] = user_id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostFeed(APIView):
    def get(self, request):
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching posts: {e}", exc_info=True)
            return Response({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentList(APIView):
    def get(self, request, post_id, *args, **kwargs):
        comments = Comment.objects.filter(post=post_id).order_by('timestamp')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id, *args, **kwargs):
        data = request.data.copy()
        data['post'] = post_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            post = get_object_or_404(Post, id=post_id)
            Notification.objects.create(
                user=post.user,
                initiator=comment.user,
                notification_type='comment',
                url_id=post_id,
                sub_url_id=comment.id
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteComment(APIView):
    def delete(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)