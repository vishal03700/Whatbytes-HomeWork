from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, PatientDoctorMappingViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'doctors', DoctorViewSet, basename='doctors')
router.register(r'mappings', PatientDoctorMappingViewSet, basename='mappings')

urlpatterns = [
    path('', include(router.urls)),
]