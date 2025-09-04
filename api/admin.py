from django.contrib import admin
from .models import Patient, Doctor, PatientDoctorMapping


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'phone', 'user', 'created_at')
    list_filter = ('age', 'created_at', 'user')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'license_number', 'years_of_experience', 'phone')
    list_filter = ('specialty', 'years_of_experience')
    search_fields = ('name', 'specialty', 'license_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'is_primary', 'assigned_date')
    list_filter = ('is_primary', 'assigned_date', 'doctor__specialty')
    search_fields = ('patient__name', 'doctor__name')
    readonly_fields = ('assigned_date',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(patient__user=request.user)