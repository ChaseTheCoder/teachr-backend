from django.shortcuts import render
from rest_framework.views import APIView
from schedules.models import SchoolDay
from schedules.serializer import SchoolDaySerializer
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
        
        queryset = SchoolDay.objects.filter(school_year=school_year_id, date__in=dates)
        serializer = SchoolDaySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)