import json
import os
import logging
import re
from dj_database_url import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import SchoolDomain
from .serializers import EmailSerializer, SchoolDomainSerializer
import openai
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

class SchoolDomainListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        school_domains = SchoolDomain.objects.all()
        serializer = SchoolDomainSerializer(school_domains, many=True)
        return Response(serializer.data)

def generate_html_message(verification_link):
    return f"""
    <html>
    <body>
    <p>Hi Teacher!</p>
    <p>Please click the following button to verify your school email:</p>
    <p><a href="{verification_link}" style="background-color: #48A94B; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Verify Your Teacher Email</a></p>
    <p>Thanks!</p>
    <p>Chase Sheaff, Founder & CEO</p>
    <p>Teacher Lounge</p>
    <p>p.s. If you have any issues with the site, want to suggest a feature, or describe what you really love about our app, feel free to reply to this email!</p>
    </body>
    </html>
    """

@permission_classes([AllowAny])
class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error(f"Invalid serializer data: {serializer.errors}")
                return Response(
                    {"status": "error", "message": serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            email = serializer.validated_data['email']
            user_id = serializer.validated_data['user_id']
            domain = email.split('@')[1]
            
            # Check existing domain
            if SchoolDomain.objects.filter(domain=domain).exists():
                existing_domain = SchoolDomain.objects.filter(domain=domain).first()
                if re.match(existing_domain.staff_email_pattern, email):
                    verification_link = "http://www.teacher-lounge.com/verify?email=" + email + "&user_id=" + user_id
                    html_message = generate_html_message(verification_link)
                    send_mail(
                        'Teacher Lounge - Verify your email so we know you are a teacher!',
                        f'Hi Teacher!\nPlease click the following link to verify your school email:\n{verification_link}\n\nThanks!\nTeacher Lounge Team',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                        html_message=html_message,
                    )
                    return Response({"status": "success", "message": "Verification email sent. Domain in DB."}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "invalid", "message": "This email appears to be a student email address."}, 
                        status=status.HTTP_400_BAD_REQUEST)
            
            # OpenAI verification
            try:
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                prompt = f"""
                Analyze if {domain} is a valid United States educational institution domain, early childhood through higher education.
                For school type the choices are: ECE, K12, HIGHER_ED.
                ECE is for Early Childhood Education, K12 is for a range within Kindergarten to 12th grade, and HIGHER_ED is for colleges and universities.
                If the domain is valid, return the following JSON object:
                {{
                    "is_valid": true/false,
                    "school": "Full school name",
                    "city": "City name",
                    "state": "State name",
                    "zip_code": "ZIP code",
                    "school_type": "K12",
                    "staff_email_pattern": ".*@domain.edu"
                }}
                """

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                
                response_text = response.choices[0].message.content.strip()
                logger.info(f"OpenAI response: {response_text}")

                try:
                    data = json.loads(response_text)
                    if not data.get('is_valid'):
                        return Response(
                            {"status": "invalid", "message": "Invalid school domain."}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Create school domain
                    school_domain = SchoolDomain.objects.create(
                        domain=domain,
                        school=data['school'],
                        city=data['city'],
                        state=data['state'],
                        zip_code=data['zip_code'],
                        school_type=data['school_type'],
                        staff_email_pattern=data.get('staff_email_pattern', f'.*@{domain}')
                    )

                    # Send verification email
                    verification_link = f"http://www.teacher-lounge.com/verify?email={email}&user_id={user_id}"
                    html_message = generate_html_message(verification_link)
                    
                    send_mail(
                        'Teacher Lounge - Verify your email so we know you are a teacher!',
                        f'Hi Teacher!\nPlease click the following link to verify your school email:\n{verification_link}\n\nThanks!\nTeacher Lounge Team',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                        html_message=html_message,
                    )
                    
                    return Response(
                        {"status": "success", "message": "Verification email sent. Domain added to DB."}, 
                        status=status.HTTP_200_OK
                    )

                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {str(e)}\nResponse: {response_text}")
                    return Response(
                        {"status": "error", "message": "Error processing OpenAI response"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            except Exception as e:
                logger.error(f"OpenAI API error: {str(e)}")
                return Response(
                    {"status": "error", "message": "Error verifying domain"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {"status": "error", "message": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )