# Generated initial migration

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Doctor's full name", max_length=100)),
                ('specialty', models.CharField(help_text="Doctor's medical specialty", max_length=100)),
                ('license_number', models.CharField(help_text="Doctor's medical license number", max_length=50, unique=True)),
                ('phone', models.CharField(help_text="Doctor's contact number", max_length=15)),
                ('email', models.EmailField(help_text="Doctor's email address", max_length=254)),
                ('years_of_experience', models.PositiveIntegerField(default=0, help_text='Years of medical experience')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Patient's full name", max_length=100)),
                ('age', models.PositiveIntegerField(help_text="Patient's age", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(150)])),
                ('address', models.TextField(help_text="Patient's address", max_length=500)),
                ('phone', models.CharField(blank=True, help_text="Patient's contact number", max_length=15)),
                ('email', models.EmailField(blank=True, help_text="Patient's email address", max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='The user who created this patient record', on_delete=django.db.models.deletion.CASCADE, related_name='patients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PatientDoctorMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
                ('is_primary', models.BooleanField(default=False, help_text="Is this the patient's primary doctor?")),
                ('notes', models.TextField(blank=True, help_text='Additional notes about the assignment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_assignments', to='api.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_assignments', to='api.patient')),
            ],
            options={
                'verbose_name': 'Patient-Doctor Assignment',
                'verbose_name_plural': 'Patient-Doctor Assignments',
                'ordering': ['-assigned_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='patientdoctormapping',
            constraint=models.UniqueConstraint(fields=('patient', 'doctor'), name='unique_patient_doctor'),
        ),
    ]