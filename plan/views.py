from django.shortcuts import render
from plan.serializers import PlansSerializer, SubjectPageSerializer, SubjectSerializer, ResourceSerializer, UnitPlanPageSerializer, UnitPlanSerializer, LessonPlanSerializer, LessonPlanDetailSerializer, MaterialSerializer, UnitPlanTitleSerializer
from .models import Subject, Resource, UnitPlan, LessonPlan, Material

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SubjectList(APIView):
  def get(self, request, *args, **kwargs):
    user_id = request.META.get('HTTP_USER_ID')
    queryset = Subject.objects.filter(user_id=user_id)
    serializer_class = SubjectPageSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
    data = {
      'subject': '', 
      'grade': '',
      'user_id': request.data.get('user_id')
    }
    serializer = SubjectSerializer(data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlansList(APIView):
  def get(self, request, *args, **kwargs):
    user_id = request.META.get('HTTP_USER_ID')
    queryset = Subject.objects.filter(user_id=user_id)
    serializer_class = PlansSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

class SubjectDetail(APIView):
  def get(self, request, subject_id, *args, **kwargs):
    queryset = Subject.objects.get(id=subject_id)
    serializer_class = SubjectSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
      'subject': '', 
      'grade': '',
      'user_id': request.data.get('user_id')
    }
    serializer = SubjectSerializer(data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, subject_id):
    instance = Subject.objects.get(id=subject_id)
    serializer = SubjectSerializer(instance, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, subject_id,  *args, **kwargs):
    instance = Subject.objects.get(id=subject_id)
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

# UNITPLAN
class UnitPlanList(APIView):
  def get(self, *args, **kwargs):
    queryset = UnitPlan.objects.all()
    serializer_class = UnitPlanSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'title': request.data.get('title'),
        'overview': '',
        'standard': '',
        'subject': request.data.get('subject'),
        'user_id': request.data.get('user_id')
    }
    serializer = UnitPlanSerializer(data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UnitPlanDetail(APIView):
  def get(self, request, unitplan_id, *args, **kwargs):
    queryset = UnitPlan.objects.get(id=unitplan_id)
    serializer_class = UnitPlanPageSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, unitplan_id,  *args, **kwargs):
    instance = UnitPlan.objects.get(id=unitplan_id)
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
  
  def post(self, request, *args, **kwargs):
    data = {
        'title': request.data.get('title'), 
        'overview': request.data.get('overview'),
        'standard': request.data.get('standard'),
        'subject': request.data.get('subject'),
        'user_id': request.data.get('user_id')
    }
    serializer = UnitPlanSerializer(data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def patch(self, request, unitplan_id):
    instance = UnitPlan.objects.get(id=unitplan_id)
    serializer = UnitPlanSerializer(instance, data=request.data, partial=True) # set partial=True to update a data partially
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LessonPlanList(APIView):
  def get(self, *args, **kwargs):
    queryset = LessonPlan.objects.all()
    serializer_class = LessonPlanSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'title': request.data.get('title'),
        'standard': '', 
        'objective': '', 
        'body': '',
        'unit_plan': request.data.get('unit_plan'),
        'user_id': request.data.get('user_id')
    }
    serializer = LessonPlanDetailSerializer(data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonPlanDetail(APIView):
  def get(self, request, lessonplan_id, *args, **kwargs):
    queryset = LessonPlan.objects.get(id=lessonplan_id)
    serializer_class = LessonPlanDetailSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, lessonplan_id,  *args, **kwargs):
    instance = LessonPlan.objects.get(id=lessonplan_id)
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
  
  def patch(self, request, lessonplan_id):
    instance = LessonPlan.objects.get(id=lessonplan_id)
    serializer = LessonPlanDetailSerializer(instance, data=request.data, partial=True) # set partial=True to update a data partially
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)