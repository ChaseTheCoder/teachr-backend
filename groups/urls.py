from django.urls import path
from .views import GroupDelete, GroupDetail, GroupJoin, GroupLeave, GroupList, GroupMembers

urlpatterns = [
    path('groups/', GroupList.as_view(), name='group-list'),
    path('group/<uuid:group_id>/', GroupDetail.as_view(), name='group-detail'),
    path('group/delete/<uuid:group_id>/', GroupDelete.as_view(), name='group-delete'),
    path('group/<uuid:group_id>/join/', GroupJoin.as_view(), name='group-join'),
    path('group/<uuid:group_id>/leave/', GroupLeave.as_view(), name='group-leave'),  
    path('group/<uuid:group_id>/admit/', GroupMembers.as_view(), name='group-admit'),  
    path('group/<uuid:group_id>/members/', GroupMembers.as_view(), name='group-members'),  
]