from rest_framework import serializers
from .models import *

class EducationStandardSerilizer(serializers.ModelSerializer):
  class Meta:
    model = EducationStandard
    fields = '__all__'

class SubjectSerilizer(serializers.ModelSerializer):
  class Meta:
    model = Subject
    fields = '__all__'

class GradeSerilizer(serializers.ModelSerializer):
  class Meta:
    model = Grade
    fields = '__all__'

class DomainSerilizer(serializers.ModelSerializer):
  class Meta:
    model = Domain
    fields = '__all__'

class StandardSerilizer(serializers.ModelSerializer):
  class Meta:
    model = Standard
    fields = '__all__'

# All
class AllDomainSerilizer(serializers.ModelSerializer):
  standards = StandardSerilizer(many=True)

  class Meta:
    model = Domain
    fields = '__all__'

class AllGradeSerilizer(serializers.ModelSerializer):
  domains = AllDomainSerilizer(many=True)

  class Meta:
    model = Grade
    fields = '__all__'

class AllSubjectSerilizer(serializers.ModelSerializer):
  grades = AllGradeSerilizer(many=True)

  class Meta:
    model = Subject
    fields = '__all__'

class AllStandardSerilizer(serializers.ModelSerializer):
  subjects = AllSubjectSerilizer(many=True)

  class Meta:
    model = Standard
    fields = '__all__'
