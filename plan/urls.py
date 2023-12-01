from django.urls import path
from . import views
from .views import LessonPlanDetail, PlanDetail, PlanList, ResourceList, UnitPlanList, UnitPlanDetail, LessonPlanList, DeleteMaterialDetail, MaterialList

urlpatterns = [
    path('plans/', views.plan, name='plan'),
    path('plan/', PlanList.as_view(), name='plans_list'),
    path('plan/<int:plan_id>/', PlanDetail.as_view(), name='plans_detail'),
    path('resource/', ResourceList.as_view(), name='resource_list'),
    path('unitplan/', UnitPlanList.as_view(), name='unit_plan_list'),
    path('unitplan/<int:unitplan_id>/', UnitPlanDetail.as_view(), name='unit_plan_detail'),
    path('lessonplan/', LessonPlanList.as_view(), name='lesson_plan_detail'),
    path('lessonplan/<int:pk>/', LessonPlanDetail.as_view(), name='lesson_plan_detail'),
    path('material/', MaterialList.as_view(), name='material_detail'),
    path('material/<int:pk>/', DeleteMaterialDetail.as_view(), name='delete_material_detail'),
    path('', views.index, name="index"),
]