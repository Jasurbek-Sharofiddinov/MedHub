from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer, DoctorSerializer, DoctorGetSerializer
from .models import MedicalProfessional
from patients.permissions import IsAuthorized, IsAdminOrReadOnly


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DoctorView(APIView):
    permission_classes = [IsAuthorized, IsAdminOrReadOnly]

    @swagger_auto_schema(responses={200: DoctorGetSerializer(many=True)})
    def get(self, request):
        doctors = MedicalProfessional.objects.all()
        serializer = DoctorGetSerializer(doctors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DoctorSerializer)
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
