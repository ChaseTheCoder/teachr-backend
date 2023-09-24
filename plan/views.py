from django.shortcuts import render
from plan.serializers import PlanSerializer, ResourceSerializer, UnitPlanSerializer, LessonPlanSerializer, LessonOutlineSerializer, MaterialSerializer
from .models import Plan, Resource, UnitPlan, LessonPlan
from django_nextjs.render import render_nextjs_page_sync
from rest_framework import generics

class PlanList(generics.ListAPIView):
  queryset = Plan.objects.all()
  serializer_class = PlanSerializer

class UnitPlanList(generics.ListAPIView):
  queryset = UnitPlan.objects.all()
  serializer_class = UnitPlanSerializer

class UnitPlanDetail(generics.RetrieveAPIView):
  queryset = UnitPlan.objects.all()
  serializer_class = UnitPlanSerializer

  # def get_queryset(self):
  #   id = self.kwargs['id']
  #   return UnitPlan.objects.filter(id=id)

class ResourceList(generics.ListAPIView):
  queryset = Resource.objects.all()
  serializer_class = ResourceSerializer

class LessonPlanList(generics.ListAPIView):
  queryset = LessonPlan.objects.all()
  serializer_class = LessonPlanSerializer

class LessonPlanDetail(generics.ListAPIView):
  queryset = LessonPlan.objects.all()
  serializer_class = LessonPlanSerializer

class LessonOutlineList(generics.ListAPIView):
  queryset = LessonPlan.objects.all()
  serializer_class = LessonOutlineSerializer

class MaterialList(generics.ListAPIView):
  queryset = LessonPlan.objects.all()
  serializer_class = MaterialSerializer

def plan(request):
  all_plans = Plan.objects.all
  return render(request, 'home.html', {'plans': all_plans})

def index(request):
    return render_nextjs_page_sync(request)