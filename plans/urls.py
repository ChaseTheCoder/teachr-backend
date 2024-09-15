from django.urls import path
from .views import LessonPlanDetail, PlansList, SubjectDetail, SubjectList, UnitPlanList, UnitPlanDetail, LessonPlanList

urlpatterns = [
    path('plans/<str:user_id>/', PlansList.as_view(), name='plans'),
    path('subjects/', SubjectList.as_view(), name='subject'),
    path('subject/', SubjectList.as_view(), name='subject_list'),
    path('subject/<str:subject_id>/', SubjectDetail.as_view(), name='subject_detail'),
    path('unit/', UnitPlanList.as_view(), name='unit_plan_list'),
    path('unit/<str:unitplan_id>/', UnitPlanDetail.as_view(), name='unit_plan_detail'),
    path('lesson/', LessonPlanList.as_view(), name='lesson_plan_detail'),
    path('lesson/<str:lessonplan_id>/', LessonPlanDetail.as_view(), name='lesson_plan_detail'),
]
urlpatterns_str = str(urlpatterns)