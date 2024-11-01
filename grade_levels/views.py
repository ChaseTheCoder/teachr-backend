from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GradeLevel
from .serializers import GradeLevelSerializer

# Create your views here.

class GradeLevelList(APIView):
  def get(self, request):
    queryset = GradeLevel.objects.all()
    serializer = GradeLevelSerializer(queryset, many=True)
    return Response(serializer.data)

  def post(self, request):
    serializer = GradeLevelSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GradeLevelDetail(APIView):
  def get_object(self, pk):
    try:
      return GradeLevel.objects.get(pk=pk)
    except GradeLevel.DoesNotExist:
      raise Http404

  def get(self, request, pk):
    grade_level = self.get_object(pk)
    serializer = GradeLevelSerializer(grade_level)
    return Response(serializer.data)

  def put(self, request, pk):
    grade_level = self.get_object(pk)
    serializer = GradeLevelSerializer(grade_level, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk):
    grade_level = self.get_object(pk)
    serializer = GradeLevelSerializer(grade_level, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    grade_level = self.get_object(pk)
    grade_level.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
