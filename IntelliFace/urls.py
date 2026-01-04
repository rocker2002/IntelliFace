"""
URL configuration for IntelliFace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "healthy", 
        "service": "IntelliFace API",
        "message": "Welcome to IntelliFace - Face Recognition Attendance System",
        "endpoints": {
            "admin": "/admin/",
            "health": "/health/",
            "api_root": "/api/",
            "login": "/api/login",
            "teachers": "/api/teacher",
            "students": "/api/student",
            "courses": "/api/course",
            "classes": "/api/class",
            "lectures": "/api/lecture"
        },
        "note": "ML features temporarily disabled for deployment"
    })

urlpatterns = [
    path('', health_check, name='health_check'),
    path('health/', health_check, name='health_check_alt'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls', namespace='users')),
]
