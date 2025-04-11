import os
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import permission_classes

from notifications.models import Notification
from user_profile.models import UserProfile
from user_profile.serializers import BasicUserProfileSerializer
from .models import Group
from .serializers import GroupListSerializer, GroupRulesSerializer, GroupSerializer
import logging

@permission_classes([IsAuthenticated])
class GroupList(APIView):
    def get(self, request):
        groups = Group.objects.all().order_by('-created_at')
        user_id = request.query_params.get('user')
        serializer = GroupListSerializer(groups, many=True, context={'request': request, 'user_id': user_id})
        return Response(serializer.data)

    def post(self, request):
        try:
            # Get the user from the request body
            user_id = request.data.get('user')
            if not user_id:
                return Response(
                    {"error": "user field is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "User not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = GroupSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                # Save the group first
                group = serializer.save()
                # Add creator as admin and member
                group.admins.add(user)
                group.members.add(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

logger = logging.getLogger(__name__)

@permission_classes([IsAuthenticated])
class GroupDetail(APIView):
    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            logger.error(f"Group with id {group_id} not found.")
            return Response(
                {"error": "Group not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        user_id = request.query_params.get('user')
        if not user_id:
            logger.error("User query parameter is missing.")
            return Response(
                {"error": "user query parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            logger.error(f"User with id {user_id} not found.")
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GroupSerializer(
            group, 
            context={'request': request, 'user_id': user_id}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response(
                {"error": "Group not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "user query parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Verify admin status
        if user not in group.admins.all():
            return Response(
                {"error": "User is not an admin of this group"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class GroupJoin(APIView):
    def patch(self, request, group_id):
        try:
            user_id = request.query_params.get('user')
            if not user_id:
                return Response(
                    {"error": "user field is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "User not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            group = Group.objects.get(id=group_id)
            if user in group.members.all():
                return Response(
                    {"error": "User is already a member of the group"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user in group.pending_members.all():
                return Response(
                    {"error": "User is already pending for group membership"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if group.is_public:
                group.members.add(user)
                return Response(
                    {"message": "User has joined the group"},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                group.pending_members.add(user)
                return Response(
                    {"message": "Membership is pending approval"}, 
                    status=status.HTTP_200_OK
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Group.DoesNotExist:
            return Response(
                {"error": "Group not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([IsAuthenticated])
class GroupLeave(APIView):
    def patch(self, request, group_id):
        try:
            user_id = request.query_params.get('user')
            if not user_id:
                return Response(
                    {"error": "user field is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "User not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            group = Group.objects.get(id=group_id)
            if user in group.members.all():
                group.members.remove(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "User is not a member of the group"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Group.DoesNotExist:
            return Response(
                {"error": "Group not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([IsAuthenticated])
class GroupDelete(APIView):
    def delete(self, request, group_id):
      try:
        user_id = request.query_params.get('user')
        if not user_id:
          return Response(
              {"error": "user field is required"}, 
              status=status.HTTP_400_BAD_REQUEST
          )

        try:
          user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
          return Response(
              {"error": "User not found"}, 
              status=status.HTTP_404_NOT_FOUND
          )

        group = Group.objects.get(id=group_id)
        if user not in group.admins.all():
          return Response(
              {"error": "User is not an admin of the group"}, 
              status=status.HTTP_403_FORBIDDEN
          )

        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      except Group.DoesNotExist:
          return Response(
              {"error": "Group not found"}, 
              status=status.HTTP_404_NOT_FOUND
          )
      except Exception as e:
          return Response(
              {"error": str(e)}, 
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )

@permission_classes([IsAuthenticated])
class GroupMembers(APIView):
    def get(self, request, group_id):
        try:
            user_id = request.query_params.get('user')
            if not user_id:
                return Response(
                    {"error": "user field is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = UserProfile.objects.get(id=user_id)
                group = Group.objects.get(id=group_id)
            except (UserProfile.DoesNotExist, Group.DoesNotExist) as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if user is admin
            if user not in group.members.all():
                return Response(
                    {"error": "User is not a member of this group"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Get admins
            admins = BasicUserProfileSerializer(
                group.admins.all().order_by('teacher_name'),
                many=True,
                context={'request': request}
            ).data

            # Get members excluding admins
            regular_members = group.members.exclude(
                id__in=group.admins.values_list('id', flat=True)
            ).order_by('teacher_name')
            members = BasicUserProfileSerializer(
                regular_members,
                many=True,
                context={'request': request}
            ).data

            if user in group.admins.all():
                pending = BasicUserProfileSerializer(
                    group.pending_members.all().order_by('teacher_name'), 
                    many=True,
                    context={'request': request}
                ).data

                return Response({
                    "admins": admins,
                    "pending": pending,
                    "members": members
                })
            else:
                return Response({
                    "admins": admins,
                    "members": members
                })

        except Exception as e:
            logger.error(f"Error in GroupMembers.get: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, group_id):
        try:
            user_id = request.query_params.get('user')
            pending_user_id = request.data.get('pending_user_id')
            admit = request.data.get('admit')

            if not all([user_id, pending_user_id, admit is not None]):
                return Response(
                    {"error": "user, pending_user_id, and admit fields are required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                admin = UserProfile.objects.get(id=user_id)
                pending_user = UserProfile.objects.get(id=pending_user_id)
                group = Group.objects.get(id=group_id)
            except (UserProfile.DoesNotExist, Group.DoesNotExist) as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Verify admin status
            if admin not in group.admins.all():
                return Response(
                    {"error": "User is not an admin of this group"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Verify pending status
            if pending_user not in group.pending_members.all():
                return Response(
                    {"error": "User is not in pending list"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Process admission/rejection
            group.pending_members.remove(pending_user)
            if admit:
                group.members.add(pending_user)
                message = f"User {pending_user.teacher_name} admitted to group"
                Notification.objects.create(
                    user=pending_user,
                    group=group,
                    notification_type='group_invite_accepted',
                    url_id=group.id,
                )
            else:
                message = f"User {pending_user.teacher_name} rejected from group"

            return Response({
                "message": message,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in GroupMembers.patch: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([IsAuthenticated])
class GroupMembersAdminRemove(APIView):
    def patch(self, request, group_id):
        try:
            user_id = request.query_params.get('user')
            remove_user_id = request.data.get('remove_user_id')

            if not all([user_id, remove_user_id]):
                return Response(
                    {"error": "user and remove_user_id fields are required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                admin = UserProfile.objects.get(id=user_id)
                remove_user = UserProfile.objects.get(id=remove_user_id)
                group = Group.objects.get(id=group_id)
            except (UserProfile.DoesNotExist, Group.DoesNotExist) as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Verify admin status
            if admin not in group.admins.all():
                return Response(
                    {"error": "User is not an admin of this group"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Verify member status
            if remove_user not in group.members.all():
                return Response(
                    {"error": "User is not a member of this group"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Remove user from members and pending_members lists
            group.members.remove(remove_user)
            group.pending_members.remove(remove_user)

            message = f"User {remove_user.teacher_name} removed from group"
            return Response({
                "message": message,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in GroupMembersAdminRemove.patch: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([IsAuthenticated])
class GroupImageUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, group_id, *args, **kwargs):
        try:
            # Get group and verify it exists
            group = get_object_or_404(Group, id=group_id)
            
            # Verify user is admin
            user_id = request.query_params.get('user_id')
            if not user_id:
                return Response(
                    {'error': 'User parameter is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return Response(
                    {'error': 'User not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            if user not in group.admins.all():
                return Response(
                    {'error': 'Only group admins can update the group profile picture'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if image was provided
            if 'profile_pic' not in request.FILES:
                return Response(
                    {'error': 'No image provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Delete old image if it exists
            if group.profile_pic:
                if os.path.isfile(group.profile_pic.path):
                    os.remove(group.profile_pic.path)

            # Save new image
            group.profile_pic = request.FILES['profile_pic']
            group.save()
            
            return Response({
                'message': 'Group profile image uploaded successfully',
                'image_url': request.build_absolute_uri(group.profile_pic.url)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error uploading group image: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([IsAuthenticated])
class GroupRules(APIView):
    def get(self, request, group_id):
        """View rules - accessible to anyone for public groups, members only for private groups"""
        try:
            group = get_object_or_404(Group, id=group_id)
            user_id = request.query_params.get('user_id')

            # For private groups, verify membership
            if not group.is_public:
                if not user_id:
                    return Response(
                        {"error": "User parameter required for private groups"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                user = get_object_or_404(UserProfile, id=user_id)
                if user not in group.members.all():
                    return Response(
                        {"error": "You must be a member to view private group rules"}, 
                        status=status.HTTP_403_FORBIDDEN
                    )

            return Response({
                "rules": group.rules or "",
                "is_admin": user_id and group.admins.filter(id=user_id).exists()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching group rules: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, group_id):
        """Update rules - admin only"""
        try:
            group = get_object_or_404(Group, id=group_id)
            user_id = request.query_params.get('user_id')
            
            if not user_id:
                return Response(
                    {"error": "User parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = get_object_or_404(UserProfile, id=user_id)
            if user not in group.admins.all():
                return Response(
                    {"error": "Only group admins can update rules"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = GroupRulesSerializer(group, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Rules updated successfully",
                    "rules": group.rules
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error updating group rules: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )