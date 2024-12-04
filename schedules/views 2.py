from venv import logger
from django.shortcuts import render
from rest_framework.views import APIView
from schedules.models import SchoolClass, SchoolDay, SchoolDayClass
from schedules.serializer import SchoolClassSerializer, SchoolDayClassSerializer, SchoolDaySerializer, SchoolDayWithClassesSerializer
from schedules.models import SchoolYear
from schedules.serializer import SchoolYearSerializer
from rest_framework.response import Response
from rest_framework import status
from user_profile.models import UserProfile

class SchoolYearList(APIView):
  def get(self, request, user_id, *args, **kwargs):
    queryset = SchoolYear.objects.filter(owner=user_id)
    serializer_class = SchoolYearSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

class SchoolYearDetail(APIView):
  def get(self, request, schedule_id, *args, **kwargs):
    try:
        school_year = SchoolYear.objects.get(id=schedule_id)
        serializer = SchoolYearSerializer(school_year)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except SchoolYear.DoesNotExist:
        return Response({"error": "SchoolYear not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def post(self, request, *args, **kwargs):
    owner_id = request.data.get('owner')

    if not owner_id:
      return Response({"error": "Owner field is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
      owner = UserProfile.objects.get(id=owner_id)
    except owner.DoesNotExist:
      return Response({"error": "No valid owner found."}, status=status.HTTP_400_BAD_REQUEST)

    data = {
      'owner': owner_id,
      'title': request.data.get('title'),
      'start_date': request.data.get('start_date'),
      'end_date': request.data.get('end_date')
    }
    serializer = SchoolYearSerializer(data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SchoolDayList(APIView):
  def get(self, request, school_year_id, *args, **kwargs):
    queryset = SchoolDay.objects.filter(school_year=school_year_id)
    serializer_class = SchoolDaySerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
      school_year_id = request.data.get('school_year')
      dates = request.data.get('dates')

      if not school_year_id or not dates:
          return Response({"error": "SchoolYear and dates fields are required."}, status=status.HTTP_400_BAD_REQUEST)

      try:
          school_year = SchoolYear.objects.get(id=school_year_id)
      except SchoolYear.DoesNotExist:
          return Response({"error": "No valid SchoolYear found."}, status=status.HTTP_400_BAD_REQUEST)

      school_days = [SchoolDay(school_year=school_year, date=date) for date in dates]
      SchoolDay.objects.bulk_create(school_days)

      return Response({"message": "SchoolDays created successfully."}, status=status.HTTP_201_CREATED)

  def delete(self, request, school_day_id, *args, **kwargs):
    try:
      school_day = SchoolDay.objects.get(id=school_day_id)
      school_day.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except SchoolDay.DoesNotExist:
      return Response({"error": "SchoolDay not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class SchoolDayRange(APIView):
  def get(self, request, school_year_id, *args, **kwargs):
    dates = request.query_params.getlist('dates')
    
    if not dates:
      return Response({"error": "Dates query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    school_days = SchoolDay.objects.filter(school_year=school_year_id, date__in=dates)
    school_day_data = []

    for school_day in school_days:
      school_day_serializer = SchoolDaySerializer(school_day)
      school_day_classes = SchoolDayClass.objects.filter(school_day=school_day.id)
      school_day_class_serializer = SchoolDayClassSerializer(school_day_classes, many=True)
      school_day_data.append({
        'school_day': school_day_serializer.data,
        'school_day_classes': school_day_class_serializer.data
      })

    return Response(school_day_data, status=status.HTTP_200_OK)
  
class SchoolDayRangeWithClasses(APIView):
  def get(self, request, school_year_id, *args, **kwargs):
    dates = request.query_params.getlist('dates')
    
    if not dates:
      return Response({"error": "Dates query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    queryset = SchoolDay.objects.filter(school_year=school_year_id, date__in=dates)
    serializer_class = SchoolDayWithClassesSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

class SchoolClassList(APIView):
    def get(self, request, school_year_id, *args, **kwargs):
        queryset = SchoolClass.objects.filter(school_year=school_year_id)
        serializer = SchoolClassSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, school_year_id, *args, **kwargs):
      titles = request.query_params.getlist('title')
      
      if not school_year_id or not titles:
        return Response({"error": "SchoolYear and titles fields are required."}, status=status.HTTP_400_BAD_REQUEST)
      
      try:
        school_year = SchoolYear.objects.get(id=school_year_id)
      except SchoolYear.DoesNotExist:
        return Response({"error": "No valid SchoolYear found."}, status=status.HTTP_400_BAD_REQUEST)
      
      school_classes = []
      for title in titles:
        if not title:
          return Response({"error": "Each class must have a title."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
          'title': title,
          'school_year': school_year_id
        }
        serializer = SchoolClassSerializer(data=data, partial=True)
        if serializer.is_valid():
          school_classes.append(serializer)
        else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      for serializer in school_classes:
        serializer.save()
      
      return Response({"message": "SchoolClasses created successfully."}, status=status.HTTP_201_CREATED)

class BulkCreateSchoolDayClassView(APIView):
    def post(self, request, school_year_id, *args, **kwargs):
        classes_by_day = request.data

        if not classes_by_day:
            return Response({"error": "classes_by_day field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            school_days = SchoolDay.objects.filter(school_year=school_year_id)
        except SchoolDay.DoesNotExist:
            return Response({"error": "No valid SchoolDays found for the given SchoolYear."}, status=status.HTTP_400_BAD_REQUEST)

        school_day_classes = []
        for school_day in school_days:
            day_of_week = school_day.date.strftime('%A').lower()
            classes = classes_by_day.get(day_of_week, [])
            for order, school_class_id in enumerate(classes, start=1):
                try:
                    school_day_classes.append(SchoolDayClass(
                        school_day=school_day,
                        school_class_id=school_class_id,
                        order=order
                    ))
                except Exception as e:
                    logger.error(f"Error creating SchoolDayClass for {school_day.date}: {e}")
                    return Response({"error": f"Error creating SchoolDayClass for {school_day.date}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            SchoolDayClass.objects.bulk_create(school_day_classes)
        except Exception as e:
            logger.error(f"Error during bulk create: {e}")
            return Response({"error": f"Error during bulk create: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "SchoolDayClasses created successfully."}, status=status.HTTP_201_CREATED)