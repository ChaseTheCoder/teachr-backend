import io
from PIL import Image
from django.shortcuts import get_object_or_404
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
            'title': request.data.get('title'),
            'profile_pic': request.data.get('profile_pic') 
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

    def delete(self, request, id, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(id=id)
            user_profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfilePicPatch(APIView):
    def patch(self, request, id, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, id=id)
        profile_pic = request.FILES.get('profile_pic')

        if profile_pic:
            # Directly pass the file to the serializer
            data = {'profile_pic': profile_pic}
            
            # Partial update
            serializer = UserProfileSerializer(user_profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Return a bad request if no file is uploaded
        return Response({"detail": "No profile_pic file uploaded."}, status=status.HTTP_400_BAD_REQUEST)