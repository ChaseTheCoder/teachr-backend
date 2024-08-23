from django.urls import path
from . import views
from .views import LessonPlanDetail, SubjectDetail, SubjectList, ResourceDetail, ResourceList, UnitPlanList, UnitPlanDetail, LessonPlanList, MaterialDetail, MaterialList

urlpatterns = [
    path('subjects/', views.subjects, name='subject'),
    path('subject/', SubjectList.as_view(), name='subject_list'),
    path('subject/<int:subject_id>/', SubjectDetail.as_view(), name='subject_detail'),
    path('unitplan/', UnitPlanList.as_view(), name='unit_plan_list'),
    path('unitplan/<int:unitplan_id>/', UnitPlanDetail.as_view(), name='unit_plan_detail'),
    path('resource/', ResourceList.as_view(), name='resource_list'),
    path('resource/<int:resource_id>/', ResourceDetail.as_view(), name='resource_detail'),
    path('lessonplan/', LessonPlanList.as_view(), name='lesson_plan_detail'),
    path('lessonplan/<int:lessonplan_id>/', LessonPlanDetail.as_view(), name='lesson_plan_detail'),
    path('material/', MaterialList.as_view(), name='material_detail'),
    path('material/<int:material_id>/', MaterialDetail.as_view(), name='delete_material_detail'),
    # path('', views.index, name="index"),
]