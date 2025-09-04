from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Patient, Doctor, PatientDoctorMapping


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with password validation.
    """
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model with validation.
    """
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate_age(self, value):
        if value < 1 or value > 150:
            raise serializers.ValidationError("Age must be between 1 and 150.")
        return value

    def validate_phone(self, value):
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Phone number must contain only digits, spaces, hyphens, and plus sign.")
        return value


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model with validation.
    """
    patient_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_patient_count(self, obj):
        return obj.patient_assignments.count()

    def validate_years_of_experience(self, value):
        if value < 0 or value > 70:
            raise serializers.ValidationError("Years of experience must be between 0 and 70.")
        return value


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient-Doctor mapping.
    """
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialty = serializers.CharField(source='doctor.specialty', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        read_only_fields = ('assigned_date',)

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if the patient belongs to the current user
        if hasattr(self, 'context') and 'request' in self.context:
            request = self.context['request']
            if patient.user != request.user:
                raise serializers.ValidationError("You can only assign doctors to your own patients.")
        
        return attrs


class PatientListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for patient list view.
    """
    doctor_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = ('id', 'name', 'age', 'phone', 'doctor_count', 'created_at')

    def get_doctor_count(self, obj):
        return obj.doctor_assignments.count()


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for doctor list view.
    """
    patient_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'specialty', 'phone', 'patient_count', 'years_of_experience')

    def get_patient_count(self, obj):
        return obj.patient_assignments.count()