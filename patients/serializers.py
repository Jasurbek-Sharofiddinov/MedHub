from rest_framework import serializers
from rest_framework.parsers import MultiPartParser
from .models import Patient, MedicalRecord
from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'date_of_birth', 'doctors', 'created_at')
        read_only_fields = ('id', 'created_at')


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
