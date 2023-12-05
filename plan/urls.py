from django.urls import path
from . import views
from .views import LessonPlanDetail, PlanDetail, PlanList, ResourceDetail, ResourceList, UnitPlanList, UnitPlanDetail, LessonPlanList, MaterialDetail, MaterialList

urlpatterns = [
    path('plans/', views.plan, name='plan'),
    path('plan/', PlanList.as_view(), name='plans_list'),
    path('plan/<int:plan_id>/', PlanDetail.as_view(), name='plans_detail'),
    path('unitplan/', UnitPlanList.as_view(), name='unit_plan_list'),
    path('unitplan/<int:unitplan_id>/', UnitPlanDetail.as_view(), name='unit_plan_detail'),
    path('resource/', ResourceList.as_view(), name='resource_list'),
    path('resource/<int:resource_id>/', ResourceDetail.as_view(), name='resource_detail'),
    path('lessonplan/', LessonPlanList.as_view(), name='lesson_plan_detail'),
    path('lessonplan/<int:lessonplan_id>/', LessonPlanDetail.as_view(), name='lesson_plan_detail'),
    path('material', MaterialList.as_view(), name='material_detail'),
    path('material/<int:material_id>/', MaterialDetail.as_view(), name='delete_material_detail'),
    path('', views.index, name="index"),
]