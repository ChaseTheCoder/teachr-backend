import json
import os
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
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user_id = serializer.validated_data['user_id']
            domain = email.split('@')[1]
            
            if SchoolDomain.objects.filter(domain=domain).exists():
                # Send verification email
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
                # Leverage OpenAI to check if the domain is valid
                client = openai.OpenAI(
                    api_key=settings.OPENAI_API_KEY,
                )
                # Use the ChatCompletion endpoint for the request
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",  # Use the appropriate model
                    messages=[
                        {"role": "user", "content": f"Is {domain} a valid United States K-12 school domain? If yes, provide the school name, city, state, and zip code in json format: school, city, state, zip_code. Else return null."}
                    ],
                    max_tokens=100,
                    temperature=0  # Setting to 0 ensures deterministic results
                )
                response_text = response.choices[0].message.content.strip()
                print(response_text)
                if response_text and response_text.lower() != 'null':
                    try:
                        data = json.loads(response_text)
                        school = data.get('school')
                        city = data.get('city')
                        state = data.get('state')
                        zip_code = data.get('zip_code')
                        if school and city and state and zip_code:
                            # Add the domain to the SchoolDomain model
                            SchoolDomain.objects.create(domain=domain, school=school, city=city, state=state, zip_code=zip_code)
                            # Send verification email
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
                            return Response({"status": "success", "message": "Verification email sent. Domain added to DB."}, status=status.HTTP_200_OK)
                    except json.JSONDecodeError:
                        pass
                else:
                    return Response({"status": "invalid", "message": "Invalid school domain."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)