"""
URL configuration for teachr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('__debug__/', include(debug_toolbar.urls)),
    path('', include('auth0authorization.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/', include('plans.urls')),
    path('v1/', include('user_profile.urls')),
    path('v1/', include('schedules.urls')),
    path('v1/', include('posts.urls')),
    path('v1/', include('notifications.urls')),
    path('v1/', include('school_domains.urls')),
    path('v1/', include('groups.urls')),
    path('v1/', include('policies.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)