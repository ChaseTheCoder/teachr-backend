from django.urls import path
from .views import SchoolDomainListView, VerifyEmailView

urlpatterns = [
    path('school_domains/', SchoolDomainListView.as_view(), name='school-domains'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]