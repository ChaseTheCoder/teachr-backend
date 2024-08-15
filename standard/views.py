from django.shortcuts import render
from standard.serializers import EducationStandardSerilizer
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class EducationStandardDetial(APIView):
  def get(self, request, education_standard_id, *args, **kwargs):
    queryset = EducationStandard.objects.get(id=education_standard_id)
    serializer_class = EducationStandardSerilizer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'education_standard': request.data.get('education_standard'),
    }
    serializer = EducationStandardSerilizer(data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, education_standard_id):
    instance = EducationStandard.objects.get(id=education_standard_id)
    serializer = EducationStandardSerilizer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, education_standard_id,  *args, **kwargs):
    instance = EducationStandard.objects.get(id=education_standard_id)
    if not instance:
        return Response(
            {"res": "Object with id does not exists"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    instance.delete()
    return Response(
      {"res": "Object deleted!"},
      status=status.HTTP_200_OK
    )