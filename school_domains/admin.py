from django.contrib import admin
from .models import SchoolDomain

@admin.register(SchoolDomain)
class SchoolDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'school', 'city', 'state', 'zip_code', 'created_at') 
    search_fields = ('domain',)