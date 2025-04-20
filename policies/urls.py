from django.urls import path
from .views import PolicyDetailView, PolicyListView, PolicyAdmin, PolicyDetailAdmin

urlpatterns = [
    path('policies/', PolicyListView.as_view()),
    path('policies/<str:url_path_name>/', PolicyDetailView.as_view()),
    path('policies/admin-view/<str:auth0>/', PolicyAdmin.as_view()),
    path('policies/<str:policy_id>/admin-view/<str:auth0>/', PolicyDetailAdmin.as_view()),
]