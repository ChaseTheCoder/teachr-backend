import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from groups.models import Group
from notifications.models import Notification
from user_profile.models import UserProfile
from .models import Grade, Post, Comment, Tag
from .serializers import GradeSerializer, PostSerializer, CommentSerializer, TagSerializer
from django.db.models import Q, Value, IntegerField
from django.db.models import Count

@permission_classes([AllowAny])
class GradeList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            grades = Grade.objects.all()
            serializer = GradeSerializer(grades, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching tags: {e}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred while fetching grades."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([AllowAny])
class TagList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            tags = Tag.objects.all()
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching tags: {e}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred while fetching tags."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TagGetOrCreate(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Get tag from request and convert to lowercase
            tag_name = request.data.get('tag', '').lower().strip()
            
            if not tag_name:
                return Response(
                    {"error": "Tag name is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Try to get existing tag or create new one
            tag, created = Tag.objects.get_or_create(
                tag=tag_name
            )

            serializer = TagSerializer(tag)
            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            
            return Response({
                "id": tag.id,
                "tag": tag.tag,
                "created": created
            }, status=status_code)

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error processing tag: {e}", exc_info=True)
            return Response(
                {"error": "An error occurred while processing the tag"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TagSearch(APIView):
    def get(self, request, *args, **kwargs):
        try:
            query = request.query_params.get('query', '').lower().strip()
            if not query:
                return Response([], status=status.HTTP_200_OK)

            matching_tags = Tag.objects.filter(
                tag__icontains=query
            ).order_by('tag')[:6]  # Limit to 6 results

            serializer = TagSerializer(matching_tags, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error searching tags: {e}", exc_info=True)
            return Response(
                {"error": "An error occurred while searching tags."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([AllowAny])
class PostByUser(APIView):
    def get(self, request, user_id, *args, **kwargs):
        posts = Post.objects.filter(user=user_id, public=True)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, *args, **kwargs):
        try:
            data = request.data.copy()
            data['user'] = user_id
            tag_ids = data.pop('tags', [])
            grade_ids = data.pop('grades', [])
            group_id = data.get('group', None)

            if group_id:
                group = get_object_or_404(Group, id=group_id)
                user = get_object_or_404(UserProfile, id=user_id)
                
                # Check if user is a member of the group
                if user not in group.members.all():
                    return Response(
                        {"error": "You must be a member of the group to post."}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Handle private group posts
                if not group.is_public:
                    data['public'] = False  # Force private for private group post

            post_serializer = PostSerializer(data=data)
            if post_serializer.is_valid():
                post = post_serializer.save()

                for tag_id in tag_ids:
                    tag = get_object_or_404(Tag, id=tag_id)
                    post.tags.add(tag)

                for grade_id in grade_ids:
                    grade = get_object_or_404(Grade, id=grade_id)
                    post.grades.add(grade)

                if group_id:
                    post.group = group
                    post.save()

                return Response(post_serializer.data, status=status.HTTP_201_CREATED)
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating post: {e}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred while creating the post."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class PostByGroup(APIView):
    def get(self, request, group_id, *args, **kwargs):
        logger = logging.getLogger(__name__)
        try:
            group = get_object_or_404(Group, id=group_id)
            user_id = request.query_params.get('user_id')
            logger.info(f"Fetching posts for group {group_id} by user {user_id}")

            if not user_id:
                return Response(
                    {"error": "User parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the actual UserProfile object
            user = get_object_or_404(UserProfile, id=user_id)

            # Check membership
            if not group.is_public and user not in group.members.all():
                logger.warning(f"Unauthorized access attempt to group {group_id} by user {user_id}")
                return Response(
                    {"error": "You do not have permission to view this group's posts."}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            posts = Post.objects.filter(group=group)
            serializer = PostSerializer(posts, many=True, context={'request': request})
            logger.info(f"Successfully fetched posts for group {group_id}")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error fetching posts for group {group_id}: {e}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred while fetching the group's posts."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([AllowAny])
class PostDetail(APIView):
    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        # Check if the post is public or if the user is a member of the group
        if not post.public:
            user_id = request.query_params.get('user_id')
            if not user_id:
                return Response({"error": "You do not have permission to view this post."}, status=status.HTTP_403_FORBIDDEN)
            
            user = get_object_or_404(UserProfile, id=user_id)
            if user not in post.group.members.all():
                return Response({"error": "You do not have permission to view this post."}, status=status.HTTP_403_FORBIDDEN)

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
            grade_ids = request.query_params.getlist('grade_ids', [])
            tag_ids = request.query_params.getlist('tag_ids', [])
            user_id = request.query_params.get('user_id')
            offset = (page - 1) * page_size

            # Base query for public posts
            base_query = Q(public=True)

            # If user is authenticated, add their group posts
            if user_id:
                user = get_object_or_404(UserProfile, id=user_id)
                user_groups = user.groups.all()
                base_query |= Q(group__in=user_groups)

            posts = Post.objects.filter(base_query).order_by('-timestamp')

            if grade_ids:
                posts = posts.filter(grades__id__in=grade_ids)

            if tag_ids:
                posts = posts.filter(tags__id__in=tag_ids)

            posts = posts.distinct().order_by('-timestamp')[offset:offset + page_size]
            serializer = PostSerializer(posts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {"error": "Invalid page or page_size parameter"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching posts: {e}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred. Please try again later."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([AllowAny])
class PostHomePage(APIView):
    def get(self, request):
        try:
            post_ids = request.query_params.getlist('post_ids')
            if not post_ids:
                return Response({"error": "No post IDs provided."}, 
                    status=status.HTTP_400_BAD_REQUEST)
            
            posts = Post.objects.filter(id__in=post_ids).order_by('-timestamp')
            serializer = PostSerializer(posts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching posts for homepage: {e}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred. Please try again later."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([AllowAny])
class CommentList(APIView):
    def get(self, request, post_id, *args, **kwargs):
        comments = Comment.objects.filter(post=post_id)\
            .annotate(upvote_count=Count('upvotes'))\
            .order_by('-upvote_count', 'timestamp')
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

@permission_classes([AllowAny])
class SearchPostsByGradesAndTags(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Get query parameters
            grade_ids = request.query_params.getlist('grade_ids', [])
            tag_ids = request.query_params.getlist('tag_ids', [])
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            
            if not grade_ids and not tag_ids:
                return Response(
                    {"error": "At least one grade_id or tag_id is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Start with all posts
            posts = Post.objects.all()

            # Filter by grades if provided
            if grade_ids:
                posts = posts.filter(grades__id__in=grade_ids)

            # Filter by tags if provided
            if tag_ids:
                posts = posts.filter(tags__id__in=tag_ids)

            # Remove duplicates and order by timestamp
            posts = posts.distinct().order_by('-timestamp')

            # Paginate results
            offset = (page - 1) * page_size
            posts = posts[offset:offset + page_size]

            serializer = PostSerializer(posts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": "Invalid page or page_size parameter"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error searching posts by grades and tags: {e}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        