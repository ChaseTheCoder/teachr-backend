from django.shortcuts import render
from .models import Plan

def plan(request):
  all_plans = Plan.objects.all
  return render(request, 'home.html', {'plans': all_plans})
