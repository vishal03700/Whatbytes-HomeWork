from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer,
    PatientSerializer,
    PatientListSerializer,
    DoctorSerializer,
    DoctorListSerializer,
    PatientDoctorMappingSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                'message': 'User registered successfully',
                'user': response.data
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({
                'error': 'Username or email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients.
    Only authenticated users can access and manage their own patients.
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'error': 'Failed to create patient',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def doctors(self, request, pk=None):
        """
        Get all doctors assigned to a specific patient.
        """
        patient = self.get_object()
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctors.
    All authenticated users can view and manage doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        return DoctorSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({
                'error': 'Doctor with this license number already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def patients(self, request, pk=None):
        """
        Get all patients assigned to a specific doctor.
        """
        doctor = self.get_object()
        mappings = PatientDoctorMapping.objects.filter(doctor=doctor)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patient-doctor assignments.
    """
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show mappings for patients owned by the current user
        return PatientDoctorMapping.objects.filter(patient__user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({
                'error': 'This patient is already assigned to this doctor'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def by_patient(self, request, patient_id=None):
        """
        Get all doctor mappings for a specific patient.
        """
        try:
            patient = Patient.objects.get(id=patient_id, user=request.user)
            mappings = PatientDoctorMapping.objects.filter(patient=patient)
            serializer = self.get_serializer(mappings, many=True)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({
                'error': 'Patient not found or you do not have permission to view this patient'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_assignment(self, request):
        """
        Remove a patient-doctor assignment.
        Expects patient_id and doctor_id in request data.
        """
        patient_id = request.data.get('patient_id')
        doctor_id = request.data.get('doctor_id')
        
        if not patient_id or not doctor_id:
            return Response({
                'error': 'Both patient_id and doctor_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            mapping = PatientDoctorMapping.objects.get(
                patient_id=patient_id,
                doctor_id=doctor_id,
                patient__user=request.user
            )
            mapping.delete()
            return Response({
                'message': 'Assignment removed successfully'
            }, status=status.HTTP_200_OK)
        except PatientDoctorMapping.DoesNotExist:
            return Response({
                'error': 'Assignment not found'
            }, status=status.HTTP_404_NOT_FOUND)