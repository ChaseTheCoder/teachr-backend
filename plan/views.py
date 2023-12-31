from authlib.integrations.django_oauth2 import ResourceProtector
from django.http import JsonResponse
from . import validator
from django.shortcuts import render
from plan.serializers import SubjectPageSerializer, SubjectSerializer, ResourceSerializer, UnitPlanPageSerializer, UnitPlanSerializer, LessonPlanSerializer, LessonOutlineSerializer, LessonPlanDetailSerializer, MaterialSerializer
from .models import Subject, Resource, UnitPlan, LessonPlan, Material

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_nextjs.render import render_nextjs_page_sync

require_auth = ResourceProtector()
validator = validator.Auth0JWTBearerTokenValidator(
    "{yourDomain}",
    "{yourApiIdentifier}"
)
require_auth.register_token_validator(validator)


def public(request):
    """No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return JsonResponse(dict(message=response))


@require_auth(None)
def private(request):
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return JsonResponse(dict(message=response))


@require_auth("read:messages")
def private_scoped(request):
    """A valid access token and an appropriate scope are required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
    return JsonResponse(dict(message=response))

# SUBJECT
class SubjectList(APIView):
  def get(self, request, *args, **kwargs):
    queryset = Subject.objects.all()
    serializer_class = SubjectPageSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def post(self, request, *args, **kwargs):
    data = {
      'subject': request.data.get('subject'), 
      'grade': request.data.get('grade')
    }
    serializer = SubjectSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectDetail(APIView):
  def get(self, request, subject_id, *args, **kwargs):
    queryset = Subject.objects.get(id=subject_id)
    serializer_class = SubjectSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, subject_id,  *args, **kwargs):
    instance = Subject.objects.get(id=subject_id)
    if not instance:
        return Response(
            {"res": "Object with id does not exists"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    instance.delete()
    return Response(
      {"res": "Object deleted!"},
      status=status.HTTP_200_OK
    )

# UNITPLAN
class UnitPlanList(APIView):
  def get(self, *args, **kwargs):
    queryset = UnitPlan.objects.all()
    serializer_class = UnitPlanSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'title': request.data.get('title'), 
        'overview': request.data.get('overview'),
        'standard': request.data.get('standard'),
        'subject': request.data.get('subject')
    }
    serializer = UnitPlanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnitPlanDetail(APIView):
  def get(self, request, unitplan_id, *args, **kwargs):
    queryset = UnitPlan.objects.get(id=unitplan_id)
    serializer_class = UnitPlanPageSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, unitplan_id,  *args, **kwargs):
    instance = UnitPlan.objects.get(id=unitplan_id)
    if not instance:
        return Response(
            {"res": "Object with id does not exists"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    instance.delete()
    return Response(
      {"res": "Object deleted!"},
      status=status.HTTP_200_OK
    )

class ResourceList(APIView):
  def get(self, *args, **kwargs):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'link': request.data.get('link'), 
        'title': request.data.get('title'),
        'unit_plan': request.data.get('unit_plan')
    }
    serializer = ResourceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class ResourceDetail(APIView):
  def get(self, request, resource_id, *args, **kwargs):
    queryset = Resource.objects.get(id=resource_id)
    serializer_class = ResourceSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, resource_id,  *args, **kwargs):
    instance = Resource.objects.get(id=resource_id)
    if not instance:
        return Response(
            {"res": "Object with id does not exists"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    instance.delete()
    return Response(
      {"res": "Object deleted!"},
      status=status.HTTP_200_OK
    )

class LessonPlanList(APIView):
  def get(self, *args, **kwargs):
    queryset = LessonPlan.objects.all()
    serializer_class = LessonPlanSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'title': request.data.get('title'),
        'standard': request.data.get('standard'), 
        'objective': request.data.get('objective'), 
        'unit_plan': request.data.get('unit_plan')
    }
    serializer = LessonPlanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonPlanDetail(APIView):
  def get(self, request, lessonplan_id, *args, **kwargs):
    queryset = LessonPlan.objects.get(id=lessonplan_id)
    serializer_class = LessonPlanDetailSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, lessonplan_id,  *args, **kwargs):
    instance = LessonPlan.objects.get(id=lessonplan_id)
    if not instance:
        return Response(
            {"res": "Object with id does not exists"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    instance.delete()
    return Response(
      {"res": "Object deleted!"},
      status=status.HTTP_200_OK
    )

class LessonOutlineList(APIView):
  def get(self, request, *args, **kwargs):
    queryset = LessonPlan.objects.all()
    serializer_class = LessonOutlineSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

class MaterialList(APIView):
  def get(self, *args, **kwargs):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'title': request.data.get('title'),
        'link': request.data.get('link'), 
        'lesson_plan': request.data.get('lesson_plan')
    }
    serializer = MaterialSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MaterialDetail(APIView):
  def get(self, request, material_id, *args, **kwargs):
    queryset = Material.objects.get(id=material_id)
    serializer_class = MaterialSerializer(queryset)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

  def delete(self, request, material_id,  *args, **kwargs):
    instance = Material.objects.get(id=material_id)
    if not instance:
        return Response(
            {"res": "Object with id does not exists"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    instance.delete()
    return Response(
      {"res": "Object deleted!"},
      status=status.HTTP_200_OK
    )

def subjects(request):
  all_subjects = Subject.objects.all
  return render(request, 'home.html', {'subjects': all_subjects})

def index(request):
    return render_nextjs_page_sync(request)

