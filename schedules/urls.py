from django.urls import path
from .views import SchoolDayList, SchoolDayRange, SchoolYearDetail, SchoolYearList

urlpatterns = [
    path('schedules/<str:user_id>', SchoolYearList.as_view(), name='schedules'),
    path('schedule', SchoolYearDetail.as_view(), name='schedule_post'),
    path('schedule/<str:schedule_id>', SchoolYearDetail.as_view(), name='schedule'),
    path('day', SchoolDayList.as_view(), name='school_day_post'),
    path('day/<str:school_day_id>', SchoolDayList.as_view(), name='school_day_delete'),
    path('days/<str:school_year_id>', SchoolDayList.as_view(), name='school_day'),
    path('days_range/<str:school_year_id>/', SchoolDayRange.as_view(), name='school_day_range'),
]
urlpatterns_str = str(urlpatterns)