from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging
import os
from urllib.parse import unquote
from django.core.exceptions import ImproperlyConfigured
from decouple import config

logger = logging.getLogger(__name__)

def verify_staff_auth0(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        try:
            # Get and decode auth0 from kwargs
            auth0 = kwargs.get('auth0')
            if auth0:
                auth0 = unquote(auth0)
            logger.debug(f"Raw auth0 from request: {auth0}")
            
            # Get allowed IDs from environment variable with better error handling
            allowed_staff = config('ALLOWED_STAFF_AUTH0_IDS')
            if not allowed_staff:
                logger.error("ALLOWED_STAFF_AUTH0_IDS environment variable is not set")
                raise ImproperlyConfigured("ALLOWED_STAFF_AUTH0_IDS environment variable is required")

            # Split and clean the auth0 IDs
            auth0_ids = [id.strip() for id in allowed_staff.split(',') if id.strip()]
            logger.debug(f"Environment variable raw value: {allowed_staff}")
            logger.debug(f"Parsed auth0_ids: {auth0_ids}")
            
            # Validate auth0 format
            if not auth0 or '|' not in auth0:
                logger.error(f"Invalid auth0 format: {auth0}")
                return Response(
                    {"error": "Invalid auth0 ID format"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if auth0 not in auth0_ids:
                logger.warning(
                    "Auth failed:\n"
                    f"Received: '{auth0}'\n"
                    f"Expected one of: {auth0_ids}\n"
                    f"Raw env value: {allowed_staff}"
                )
                return Response(
                    {"error": "Unauthorized access"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            logger.info(f"Authorization successful for auth0: {auth0}")
            return view_func(self, request, *args, **kwargs)
            
        except ImproperlyConfigured as e:
            logger.error(str(e))
            return Response(
                {"error": "Server configuration error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error in staff verification: {str(e)}", exc_info=True)
            return Response(
                {"error": "An error occurred during authorization"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper