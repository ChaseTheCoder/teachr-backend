from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Policy
from .serializers import PolicyAdminSerializer, PolicyListSerializer, PolicySerializer
from .decorators import verify_staff_auth0
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@permission_classes([AllowAny])
class PolicyListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            policies = Policy.objects.all()
            serializer = PolicyListSerializer(policies, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching policies: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching policies"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([AllowAny])
class PolicyDetailView(APIView):
  def get(self, request, url_path_name, *args, **kwargs):
    try:
      policy = Policy.objects.filter(url_path_name=url_path_name).first()
      if not policy:
        return Response(
          {"error": "Policy not found"},
          status=status.HTTP_404_NOT_FOUND
        )
      serializer = PolicySerializer(policy)
      return Response(serializer.data)
    except Exception as e:
      logger.error(f"Error fetching policy: {str(e)}")
      return Response(
        {"error": "An error occurred while fetching the policy"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )

@permission_classes([IsAuthenticated])
class PolicyAdmin(APIView):
    @verify_staff_auth0
    def get(self, request, *args, **kwargs):
        try:
            policies = Policy.objects.all()
            serializer = PolicyAdminSerializer(policies, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching policies: {str(e)}")
            return Response(
                {"error": "An error occurred while fetching policies"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @verify_staff_auth0
    def post(self, request, auth0, *args, **kwargs):
        try:
            serializer = PolicySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating policy: {str(e)}")
            return Response(
                {"error": "An error occurred while creating the policy"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@permission_classes([IsAuthenticated])
class PolicyDetailAdmin(APIView):
    @verify_staff_auth0
    def patch(self, request, policy_id, auth0):
        try:
            try:
                policy = Policy.objects.get(id=policy_id)
            except Policy.DoesNotExist:
                return Response(
                    {"error": "Policy not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            if not policy:
                return Response(
                    {"error": "Policy not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = PolicyAdminSerializer(policy, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating policy: {str(e)}")
            return Response(
                {"error": "An error occurred while updating the policy"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )