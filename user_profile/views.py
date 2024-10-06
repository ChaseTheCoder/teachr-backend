from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserProfileGetPost(APIView):
    def get(self, request, auth0_id, *args, **kwargs):
        try:
            queryset = UserProfile.objects.get(auth0_id=auth0_id)
            serializer_class = UserProfileSerializer(queryset)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"user_profile error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, auth0_id, *args, **kwargs):
        data = {
            'auth0_id': auth0_id,
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'teacher_name': request.data.get('teacher_name'),
        }
        serializer = UserProfileSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdate(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            queryset = UserProfile.objects.get(id=id)
            serializer_class = UserProfileSerializer(queryset)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"user_profile error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id):
        instance = UserProfile.objects.get(id=id)
        serializer = UserProfileSerializer(instance, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)