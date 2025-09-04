from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Patient(models.Model):
    """
    Patient model linked to the user who created it.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='patients',
        help_text="The user who created this patient record"
    )
    name = models.CharField(
        max_length=100,
        help_text="Patient's full name"
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(150)],
        help_text="Patient's age"
    )
    address = models.TextField(
        max_length=500,
        help_text="Patient's address"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        help_text="Patient's contact number"
    )
    email = models.EmailField(
        blank=True,
        help_text="Patient's email address"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return f"{self.name} (Age: {self.age})"


class Doctor(models.Model):
    """
    Doctor model for healthcare professionals.
    """
    name = models.CharField(
        max_length=100,
        help_text="Doctor's full name"
    )
    specialty = models.CharField(
        max_length=100,
        help_text="Doctor's medical specialty"
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Doctor's medical license number"
    )
    phone = models.CharField(
        max_length=15,
        help_text="Doctor's contact number"
    )
    email = models.EmailField(
        help_text="Doctor's email address"
    )
    years_of_experience = models.PositiveIntegerField(
        default=0,
        help_text="Years of medical experience"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"


class PatientDoctorMapping(models.Model):
    """
    Model to map patients to their assigned doctors.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='doctor_assignments'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patient_assignments'
    )
    assigned_date = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(
        default=False,
        help_text="Is this the patient's primary doctor?"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the assignment"
    )

    class Meta:
        unique_together = ['patient', 'doctor']
        ordering = ['-assigned_date']
        verbose_name = 'Patient-Doctor Assignment'
        verbose_name_plural = 'Patient-Doctor Assignments'

    def __str__(self):
        return f"{self.patient.name} → Dr. {self.doctor.name}"