import io
from rest_framework.parsers import MultiPartParser, FormParser
import os
from PIL import Image
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer, BasicUserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

@permission_classes([AllowAny])
class UserProfileGetPost(APIView):
    def get(self, request, auth0_id, *args, **kwargs):
        try:
            queryset = UserProfile.objects.get(auth0_id=auth0_id)
            serializer_class = UserProfileSerializer(queryset, context={'request': request})
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

@permission_classes([AllowAny])
class UserProfileUpdate(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            queryset = UserProfile.objects.get(id=id)
            serializer_class = UserProfileSerializer(queryset, context={'request': request})
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"user_profile error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id):
        instance = UserProfile.objects.get(id=id)
        serializer = UserProfileSerializer(instance, data=request.data, context={'request': request}, partial=True) 
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

@permission_classes([AllowAny])
class UserProfileBatchList(APIView):
    def get(self, request, *args, **kwargs):
        ids = request.query_params.getlist('user_id')
        if not ids:
            return Response({"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter UserProfile objects by the provided IDs
        queryset = UserProfile.objects.filter(id__in=ids)
        serializer = BasicUserProfileSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileList(APIView):
    def get(self, request, *args, **kwargs):
        queryset = UserProfile.objects.all()
        serializer = UserProfileSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@permission_classes([AllowAny])
class VerifyProfile(APIView):
    def patch(self, request, id, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, id=id)
        verified_email = request.data.get('verified_email')
        
        if not verified_email:
            return Response({"detail": "verified_email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user_profile.verified = True
        user_profile.email_domain = verified_email.split('@')[1]
        user_profile.verified_email = verified_email
        user_profile.save()
        
        return Response({"detail": "Profile verified."}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class ProfileImageUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, id, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, id=id)
        
        if 'profile_pic' not in request.FILES:
            return Response(
                {'error': 'No image provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Delete old image if it exists
        if user_profile.profile_pic:
            if os.path.isfile(user_profile.profile_pic.path):
                os.remove(user_profile.profile_pic.path)

        try:
            # Save the new profile picture
            user_profile.profile_pic = request.FILES['profile_pic']
            user_profile.save()

            # Add a version query parameter to the image URL to force React-Query to fetch the updated image
            image_url = f"{request.build_absolute_uri(user_profile.profile_pic.url)}?v={int(user_profile.updated_at.timestamp())}"

            return Response({
                'message': 'Profile image uploaded successfully',
                'image_url': image_url
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )