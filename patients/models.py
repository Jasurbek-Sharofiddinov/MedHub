from django.db import models
from django.utils import timezone


class Patient(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    doctors = models.ManyToManyField('doctors.MedicalProfessional', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}'.format(self.name)


class MedicalRecord(models.Model):
    HEALTHY = 'HE'
    UNCHECKED = 'UC'
    UNHEALTHY = 'UH'
    IN_HOSPITAL = 'IH'
    MEDICAL_CONDITION_CHOICES = [
        (HEALTHY, 'Healthy'),
        (UNCHECKED, 'Unchecked'),
        (UNHEALTHY, 'Unhealthy'),
        (IN_HOSPITAL, 'In Hospital'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    medical_condition = models.CharField(max_length=2, choices=MEDICAL_CONDITION_CHOICES)
    medical_record = models.FileField(upload_to='static/medical_files/', null=True, blank=True)
    x_ray = models.ImageField(upload_to='static/x_rays/', null=True, blank=True)
    medical_image = models.ImageField(upload_to='static/medical_images/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
