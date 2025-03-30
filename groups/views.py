from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import permission_classes

from user_profile.models import UserProfile
from .models import Group
from .serializers import GroupListSerializer, GroupSerializer
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