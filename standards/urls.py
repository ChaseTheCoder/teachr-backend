from django.urls import path
from .views import DomainBulkPost, DomainList, GradeLevelsList, IssuingAuthorityList, IssuingAuthorityDetail, SubjectList

urlpatterns = [
    path('issuing_authority/', IssuingAuthorityList.as_view(), name='issuingauthority-list'),
    path('issuing_authority/<str:pk>/', IssuingAuthorityDetail.as_view(), name='issuingauthority-detail'),
    path('standard_subjects/<str:pk>/', SubjectList.as_view()),
    path('standard_grades/<str:pk>/', GradeLevelsList.as_view()),
    path('standard_domains/<str:pk>/', DomainList.as_view()),
    path('standard_domains/', DomainBulkPost.as_view()),
]