from django.shortcuts import render
from plan import serializers
from plan.serializers import PlanSerializer, ResourceSerializer, UnitPlanSerializer, LessonPlanSerializer, LessonOutlineSerializer, MaterialSerializer
from .models import Plan, Resource, UnitPlan, LessonPlan, Material

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django_nextjs.render import render_nextjs_page_sync
from rest_framework import generics

class PlanList(APIView):
  def get(self, *args, **kwargs):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer(queryset, many=True)
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
        'subject': request.subject.id
    }
    serializer = UnitPlanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnitPlanDetail(generics.RetrieveAPIView):
  queryset = UnitPlan.objects.all()
  serializer_class = UnitPlanSerializer

class ResourceList(generics.ListAPIView):
  queryset = Resource.objects.all()
  serializer_class = ResourceSerializer

class LessonPlanList(generics.ListAPIView):
  queryset = LessonPlan.objects.all()
  serializer_class = LessonPlanSerializer

class LessonPlanDetail(generics.RetrieveAPIView):
  queryset = LessonPlan.objects.all()
  serializer_class = LessonPlanSerializer

class LessonOutlineList(generics.ListAPIView):
  queryset = LessonPlan.objects.all()
  serializer_class = LessonOutlineSerializer

class MaterialList(generics.ListAPIView):
  queryset = Material.objects.all()
  serializer_class = MaterialSerializer

class DeleteMaterialDetail(generics.DestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

def plan(request):
  all_plans = Plan.objects.all
  return render(request, 'home.html', {'plans': all_plans})

def index(request):
    return render_nextjs_page_sync(request)

