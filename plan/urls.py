from django.urls import path
from . import views
from .views import PlanList

urlpatterns = [
    path('plan/', views.plan, name='plan'),
    path('plans/', PlanList.as_view(), name='plans_list'),
    path('', views.index, name="index"),
]