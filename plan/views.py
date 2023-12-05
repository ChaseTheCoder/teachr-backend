from django.shortcuts import get_object_or_404, render
from plan import serializers
from plan.serializers import PlanPageSerializer, PlanSerializer, ResourceSerializer, UnitPlanSerializer, LessonPlanSerializer, LessonOutlineSerializer, LessonPlanDetailSerializer, MaterialSerializer
from .models import Plan, Resource, UnitPlan, LessonPlan, Material

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django_nextjs.render import render_nextjs_page_sync
from rest_framework import generics

# PLAN
class PlanList(APIView):
  def get(self, request, *args, **kwargs):
    queryset = Plan.objects.all()
    serializer_class = PlanPageSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
    data = {
      'subject': request.data.get('subject'), 
      'grade': request.data.get('grade')
    }
    serializer = PlanSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlanDetail(APIView):
  def get(self, request, plan_id, *args, **kwargs):
    queryset = Plan.objects.get(id=plan_id)
    serializer_class = PlanSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, plan_id,  *args, **kwargs):
    instance = Plan.objects.get(id=plan_id)
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
        'overview': request.data.get('overview'),
        'standard': request.data.get('standard'),
        'subject': request.data.get('subject')
    }
    serializer = UnitPlanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnitPlanDetail(APIView):
  def get(self, request, unitplan_id, *args, **kwargs):
    queryset = UnitPlan.objects.get(id=unitplan_id)
    serializer_class = UnitPlanSerializer(queryset)
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

class ResourceList(APIView):
  def get(self, *args, **kwargs):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'link': request.data.get('link'), 
        'title': request.data.get('title'),
        'unit_plan': request.data.get('unit_plan')
    }
    serializer = ResourceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class ResourceDetail(APIView):
  def get(self, request, resource_id, *args, **kwargs):
    queryset = Resource.objects.get(id=resource_id)
    serializer_class = ResourceSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, resource_id,  *args, **kwargs):
    instance = Resource.objects.get(id=resource_id)
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

class LessonPlanList(generics.ListAPIView):
  def get(self, *args, **kwargs):
    queryset = LessonPlan.objects.all()
    serializer_class = LessonPlanSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'title': request.data.get('title'),
        'standard': request.data.get('standard'), 
        'objective': request.data.get('objective'), 
        'unit_plan': request.data.get('unit_plan')
    }
    serializer = LessonPlanDetailSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonPlanDetail(generics.RetrieveAPIView):
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

class LessonOutlineList(generics.ListAPIView):
  queryset = LessonPlan.objects.all()
  serializer_class = LessonOutlineSerializer

class MaterialList(generics.ListAPIView):
  def get(self, *args, **kwargs):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'title': request.data.get('title'),
        'link': request.data.get('link'), 
        'lesson_plan': request.data.get('lesson_plan')
    }
    serializer = MaterialSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteMaterialDetail(generics.DestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

def plan(request):
  all_plans = Plan.objects.all
  return render(request, 'home.html', {'plans': all_plans})

def index(request):
    return render_nextjs_page_sync(request)

