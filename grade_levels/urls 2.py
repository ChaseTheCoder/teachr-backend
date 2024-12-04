from django.urls import path
from .views import GradeLevelList, GradeLevelDetail

urlpatterns = [
    path('grade_levels/', GradeLevelList.as_view(), name='gradelevel-list'),
    path('grade_levels/<str:pk>/', GradeLevelDetail.as_view(), name='gradelevel-detail'),
]