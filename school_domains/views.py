from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import SchoolDomain
from .serializers import EmailSerializer

@permission_classes([AllowAny])
class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user_id = serializer.validated_data['user_id']
            domain = email.split('@')[1]
            
            if SchoolDomain.objects.filter(domain=domain).exists() or domain == 'teacher-lounge.com':
                # Send verification email
                verification_link = "http://www.teacher-lounge.com/verify?email=" + email + "&user_id=" + user_id
                html_message = f"""
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
                send_mail(
                    'Teacher Lounge - Verify your email so we know you are a teacher!',
                    f'Hi Teacher!\nPlease click the following link to verify your school email:\n{verification_link}\n\nThanks!\nTeacher Lounge Team',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                    html_message=html_message,
                )
                return Response({"message": "Verification email sent."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid school domain."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)