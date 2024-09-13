from django.urls import path
from . import views
from .views import LessonPlanDetail, PlansList, SubjectDetail, SubjectList, UnitPlanList, UnitPlanDetail, LessonPlanList

urlpatterns = [
    path('plans/', PlansList.as_view(), name='plans'),
    path('subjects/', views.subjects, name='subject'),
    path('subject/', SubjectList.as_view(), name='subject_list'),
    path('subject/<int:subject_id>/', SubjectDetail.as_view(), name='subject_detail'),
    path('unitplan/', UnitPlanList.as_view(), name='unit_plan_list'),
    path('unitplan/<int:unitplan_id>/', UnitPlanDetail.as_view(), name='unit_plan_detail'),
    path('lessonplan/', LessonPlanList.as_view(), name='lesson_plan_detail'),
    path('lessonplan/<int:lessonplan_id>/', LessonPlanDetail.as_view(), name='lesson_plan_detail'),
    # path('', views.index, name="index"),
]