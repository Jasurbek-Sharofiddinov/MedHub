from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema

from .models import Patient, MedicalRecord
from .serializers import PatientSerializer, MedicalRecordSerializer
from .permissions import IsAuthorized, IsAdminOrReadOnly


@swagger_auto_schema(request_body=PatientSerializer)
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthorized, IsAdminOrReadOnly]
    filterset_fields = ['name', 'date_of_birth', 'medical_records__medical_condition']

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthorized]
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return MedicalRecord.objects.filter(patient__doctors__user__id=self.request.user.id)

    @action(detail=True, methods=['get'])
    def dl_med_record(self, request, pk=None):
        try:
            medical_record = self.get_object()
            file_path = medical_record.medical_record.path
            with open(file_path, 'rb') as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{medical_record.medical_record.name}"'
            return response
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def dl_med_image(self, request, pk=None):
        try:
            medical_record = self.get_object()
            file_path = medical_record.medical_image.path
            with open(file_path, 'rb') as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{medical_record.medical_image.name}"'
            return response
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def dl_x_ray(self, request, pk=None):
        try:
            medical_record = self.get_object()
            file_path = medical_record.x_ray.path
            with open(file_path, 'rb') as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{medical_record.x_ray.name}"'
            return response
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
