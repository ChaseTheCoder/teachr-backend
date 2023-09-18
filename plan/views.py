from django.shortcuts import render
from plan.serializers import PlanSerializer
from .models import Plan
from django_nextjs.render import render_nextjs_page_sync
from rest_framework import generics

class PlanList(generics.ListAPIView):
   queryset = Plan.objects.all()
   serializer_class = PlanSerializer

def plan(request):
  all_plans = Plan.objects.all
  return render(request, 'home.html', {'plans': all_plans})

def index(request):
    return render_nextjs_page_sync(request)