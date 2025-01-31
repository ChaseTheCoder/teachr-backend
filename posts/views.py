import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from notifications.models import Notification
from user_profile.models import UserProfile
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Q, Value, IntegerField

@permission_classes([AllowAny])
class PostByUser(APIView):
    def get(self, request, user_id, *args, **kwargs):
        posts = Post.objects.filter(user=user_id)
        serializer = PostSerializer(posts, many=True, context={'request': request})
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

@permission_classes([AllowAny])
class PostDetail(APIView):
    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([AllowAny])
class PostFeed(APIView):
    def get(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            offset = (page - 1) * page_size
            posts = Post.objects.all().order_by('-timestamp')[offset:offset + page_size]
            serializer = PostSerializer(posts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching posts: {e}", exc_info=True)
            return Response({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([AllowAny])
class CommentList(APIView):
    def get(self, request, post_id, *args, **kwargs):
        comments = Comment.objects.filter(post=post_id).order_by('timestamp')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id, *args, **kwargs):
        data = request.data.copy()
        data['post'] = post_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            post = get_object_or_404(Post, id=post_id)
            if post.user != comment.user:
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
    
@permission_classes([AllowAny])
class SearchPosts(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('search', '')
        if not query:
            return Response({"error": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        offset = (page - 1) * page_size

        title_matches = Post.objects.filter(title__icontains=query).annotate(rank=Value(1, output_field=IntegerField()))
        words = query.split()
        additional_title_matches = Post.objects.none()
        for word in words:
            additional_title_matches = additional_title_matches.union(
            Post.objects.filter(title__icontains=word).exclude(id__in=title_matches.values_list('id', flat=True)).annotate(rank=Value(1, output_field=IntegerField()))
            )
        body_matches = Post.objects.filter(body__icontains=query).exclude(id__in=title_matches.values_list('id', flat=True)).exclude(id__in=additional_title_matches.values_list('id', flat=True)).annotate(rank=Value(2, output_field=IntegerField()))
        additional_body_matches = Post.objects.none()
        for word in words:
            additional_body_matches = additional_body_matches.union(
            Post.objects.filter(body__icontains=word).exclude(id__in=title_matches.values_list('id', flat=True)).exclude(id__in=additional_title_matches.values_list('id', flat=True)).exclude(id__in=body_matches.values_list('id', flat=True)).annotate(rank=Value(2, output_field=IntegerField()))
            )
        
        posts = title_matches.union(body_matches).union(additional_title_matches).union(additional_body_matches).order_by('rank', '-timestamp')[offset:offset + page_size]
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdatePostVote(APIView):
    def patch(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        user_id = request.data.get('user')
        action = request.data.get('action')
        
        if not user_id or not action:
            return Response({"status": "error", "message": "User and action are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(UserProfile, id=user_id)
        
        if action == 'upvote':
            if user in post.upvotes.all():
                post.upvotes.remove(user)
            else:
                post.upvotes.add(user)
                if user in post.downvotes.all():
                    post.downvotes.remove(user)
                if post.user.id != user_id:
                    Notification.objects.update_or_create(
                        notification_type='upvote_post',
                        user=post.user,
                        url_id=str(post_id),
                        sub_url_id=None,
                        defaults={
                            'read': False,
                        }
                    )
        elif action == 'downvote':
            if user in post.downvotes.all():
                post.downvotes.remove(user)
            else:
                post.downvotes.add(user)
                if user in post.upvotes.all():
                    post.upvotes.remove(user)
        else:
            return Response({"status": "error", "message": "Invalid vote type."}, status=status.HTTP_400_BAD_REQUEST)
        
        post.save()
        return Response({"status": "success", "message": "Post vote successful."}, status=status.HTTP_200_OK)

class UpdateCommentVote(APIView):
    def patch(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        user_id = request.data.get('user')
        action = request.data.get('action')

        if not user_id or not action:
            return Response({"status": "error", "message": "User and action are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(UserProfile, id=user_id)
        
        if action == 'upvote':
            if user in comment.upvotes.all():
                comment.upvotes.remove(user)
            else:
                comment.upvotes.add(user)
                if user in comment.downvotes.all():
                    comment.downvotes.remove(user)
                if comment.user.id != user_id:
                    Notification.objects.update_or_create(
                        notification_type='upvote_comment',
                        user=comment.user,
                        url_id=str(comment.post.id),
                        sub_url_id=str(comment.id),
                        defaults={
                            'read': False,
                        }
                    )
        elif action == 'downvote':
            if user in comment.downvotes.all():
                comment.downvotes.remove(user)
            else:
                comment.downvotes.add(user)
                if user in comment.upvotes.all():
                    comment.upvotes.remove(user)
        else:
            logger = logging.getLogger(__name__)
            logger.error(f"Invalid vote type: {action} for user: {user_id} on comment: {comment_id}")
            return Response({"status": "error", "message": "Invalid vote type."}, status=status.HTTP_400_BAD_REQUEST)
        
        comment.save()
        return Response({"status": "success", "message": "Comment vote successful."}, status=status.HTTP_200_OK)