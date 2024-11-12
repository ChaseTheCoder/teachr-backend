from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GradeLevels, IssuingAuthority, Subject, Domain, Standard
from .serializers import IssuingAuthoritySerializer, GradeLevelsSerializer, SubjectSerializer, DomainSerializer, StandardSerializer, SubjectSerializerList

class IssuingAuthorityList(APIView):
  def get(self, request, pk=None):
    if pk:
      issuing_authority = get_object_or_404(IssuingAuthority, pk=pk)
      serializer = IssuingAuthoritySerializer(issuing_authority)
    else:
      issuing_authorities = IssuingAuthority.objects.all()
      serializer = IssuingAuthoritySerializer(issuing_authorities, many=True)
    return Response(serializer.data)

  def post(self, request):
    serializer = IssuingAuthoritySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssuingAuthorityDetail(APIView):
  def patch(self, request, pk):
    issuing_authority = get_object_or_404(IssuingAuthority, pk=pk)
    serializer = IssuingAuthoritySerializer(issuing_authority, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    issuing_authority = get_object_or_404(IssuingAuthority, pk=pk)
    issuing_authority.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class SubjectList(APIView):
  def get(self, request, pk):
    subjects = Subject.objects.filter(issuing_authority__pk=pk)
    serializer = SubjectSerializerList(subjects, many=True)
    return Response(serializer.data)

  def post(self, request, pk):
    issuing_authority = get_object_or_404(IssuingAuthority, pk=pk)
    subjects_data = request.data
    created_subjects = []

    for subject_data in subjects_data:
      subject_data['issuing_authority'] = issuing_authority.id
      serializer = SubjectSerializer(data=subject_data)
      if serializer.is_valid():
        serializer.save()
        created_subjects.append(serializer.data)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(created_subjects, status=status.HTTP_201_CREATED)

  def patch(self, request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    serializer = SubjectSerializer(subject, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class GradeLevelsList(APIView):
  def get(self, request, pk):
    grade_levels = GradeLevels.objects.filter(subject__pk=pk)
    serializer = GradeLevelsSerializer(grade_levels, many=True)
    return Response(serializer.data)

  def post(self, request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    grade_levels_data = request.data
    created_grade_levels = []

    for grade_level_data in grade_levels_data:
      grade_level_data['subject'] = subject.id
      serializer = GradeLevelsSerializer(data=grade_level_data)
      if serializer.is_valid():
        serializer.save()
        created_grade_levels.append(serializer.data)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(created_grade_levels, status=status.HTTP_201_CREATED)

  def patch(self, request, pk):
    grade_level = get_object_or_404(GradeLevels, pk=pk)
    serializer = GradeLevelsSerializer(grade_level, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    grade_level = get_object_or_404(GradeLevels, pk=pk)
    grade_level.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class DomainList(APIView):
  def get(self, request, pk):
    domains = Domain.objects.filter(grade_levels__pk=pk)
    serializer = DomainSerializer(domains, many=True)
    return Response(serializer.data)

  def patch(self, request, pk):
    domain = get_object_or_404(Domain, pk=pk)
    serializer = DomainSerializer(domain, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    domain = get_object_or_404(Domain, pk=pk)
    domain.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class DomainBulkPost(APIView):
  def post(self, request):
    domains_data = request.data
    created_domains = []

    for domain_data in domains_data:
      serializer = DomainSerializer(data=domain_data)
      if serializer.is_valid():
        serializer.save()
        created_domains.append(serializer.data)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(created_domains, status=status.HTTP_201_CREATED)