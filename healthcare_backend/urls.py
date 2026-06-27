"""
Root URL configuration for the healthcare_backend project.

URL layout:
    /admin/                -> Django admin
    /api/health/           -> simple health check
    /api/auth/             -> register / login (accounts app)
    /api/patients/         -> patient CRUD (patients app)
    /api/doctors/          -> doctor CRUD (doctors app)
    /api/mappings/         -> patient-doctor mapping (mappings app)
"""

from django.contrib import admin
from django.urls import include, path

from core.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/auth/', include('accounts.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/mappings/', include('mappings.urls')),
]
