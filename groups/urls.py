from django.urls import path
from .views import GroupDelete, GroupDetail, GroupImageUpload, GroupJoin, GroupLeave, GroupList, GroupMembers, GroupMembersAdminRemove, GroupRules

urlpatterns = [
    path('groups/', GroupList.as_view(), name='group-list'),
    path('group/<uuid:group_id>/', GroupDetail.as_view(), name='group-detail'),
    path('group/delete/<uuid:group_id>/', GroupDelete.as_view(), name='group-delete'),
    path('group/<uuid:group_id>/join/', GroupJoin.as_view(), name='group-join'),
    path('group/<uuid:group_id>/leave/', GroupLeave.as_view(), name='group-leave'),  
    path('group/<uuid:group_id>/admit/', GroupMembers.as_view(), name='group-admit'),  
    path('group/<uuid:group_id>/members/', GroupMembers.as_view(), name='group-members'),
    path('group/<uuid:group_id>/members/remove/', GroupMembersAdminRemove.as_view(), name='group-remove-members'),
    path('group/<uuid:group_id>/image/', GroupImageUpload.as_view(), name='group-image-upload'),
    path('group/<uuid:group_id>/rules/', GroupRules.as_view(), name='group-rules'),
]