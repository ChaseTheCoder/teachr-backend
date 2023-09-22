from django.urls import path
from . import views
from .views import PlanList, ResourceList, UnitPlanList, LessonPlanList

urlpatterns = [
    path('plans/', views.plan, name='plan'),
    path('plan/', PlanList.as_view(), name='plans_list'),
    path('resource/', ResourceList.as_view(), name='resource_list'),
    path('unitplan/', UnitPlanList.as_view(), name='unit_plan_list'),
    path('lessonplan/', LessonPlanList.as_view(), name='lesson_plan_list'),
    path('', views.index, name="index"),
]