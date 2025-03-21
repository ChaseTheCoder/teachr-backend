from django.utils import timezone
import uuid
from django.db import models

SCHOOL_TYPE_CHOICES = [
    ('ECE', 'Early Childhood Center'),
    ('K12', 'K-12'),
    ('HIGHER_ED', 'Higher Education'),
]

class SchoolDomain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    domain = models.CharField(max_length=255, unique=True)
    school = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    school_type = models.CharField(max_length=10, choices=SCHOOL_TYPE_CHOICES, default='K12')
    staff_email_pattern = models.CharField(max_length=255, blank=True, null=True, help_text="Regex pattern for staff emails", default='.*@cps.edu')
    created_at = models.DateTimeField(auto_now_add=True)