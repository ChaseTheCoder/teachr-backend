from django.shortcuts import render
from .models import Plan
from django_nextjs.render import render_nextjs_page_sync

def plan(request):
  all_plans = Plan.objects.all
  return render(request, 'home.html', {'plans': all_plans})

def index(request):
    return render_nextjs_page_sync(request)