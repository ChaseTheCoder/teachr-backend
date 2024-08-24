
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileDetail(APIView):
	def get(self, request, *args, **kwargs):
		user_profile = UserProfile.objects.get(user=request.user)
		serializer = UserProfileSerializer(user_profile)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		data = {
			'auth0_user_id': request.data.get('auth0_user_id'),
			'first_name': request.data.get('first_name'),
			'last_name': request.data.get('last_name'),
			'teacher_name': request.data.get('teacher_name'),
			'title': request.data.get('title')
		}
		serializer = UserProfileSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, *args, **kwargs):
		user_profile = UserProfile.objects.get(user=request.user)
		data = {
			'first_name': request.data.get('first_name'),
			'last_name': request.data.get('last_name'),
			'teacher_name': request.data.get('teacher_name'),
			'title': request.data.get('title')
		}
		serializer = UserProfileSerializer(user_profile, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, *args, **kwargs):
		user_profile = UserProfile.objects.get(user=request.user)
		user_profile.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)