from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, MedicalRecordViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'medical-records', MedicalRecordViewSet, basename='medical_records')

urlpatterns = [
    path('', include(router.urls)),
]
