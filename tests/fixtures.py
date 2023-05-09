import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from patients.models import Patient, MedicalRecord
from doctors.models import MedicalProfessional

user = get_user_model()


@pytest.fixture
def user1():
    return user.objects.create_user(
        username='testuser1',
        password='12345'
    )


@pytest.fixture
def user2():
    return user.objects.create_user(
        username='testuser2',
        password='12345'
    )


@pytest.fixture
def user3():
    return user.objects.create_user(
        username='testuser3',
        password='12345'
    )


@pytest.fixture
def admin_user():
    return user.objects.create_superuser(
        username='admin',
        password='admin',
    )

@pytest.fixture
def med_professional1(user1):
    return MedicalProfessional.objects.create(user=user1)


@pytest.fixture
def med_professional2(user2):
    return MedicalProfessional.objects.create(user=user2)


@pytest.fixture
def patient1(med_professional1):
    patient = Patient.objects.create(
        name='John Doe',
        date_of_birth='1990-01-01',
    )
    patient.doctors.add(med_professional1)
    patient.save()
    return patient


@pytest.fixture
def patient2(med_professional2):
    patient = Patient.objects.create(
        name='Jane Doe',
        date_of_birth='1990-01-01',
    )
    patient.doctors.add(med_professional2)
    patient.save()
    return patient


@pytest.fixture
def medical_record1(patient1):
    return MedicalRecord.objects.create(
        patient=patient1,
        medical_condition='UH',
        medical_record=SimpleUploadedFile('test_record1.txt', b'medical_record1', content_type='text/plain')
    )


@pytest.fixture
def medical_record11(patient1):
    return MedicalRecord.objects.create(
        patient=patient1,
        medical_condition='HE',
        medical_record=SimpleUploadedFile('test_record11.txt', b'medical_record11', content_type='text/plain')
        )


@pytest.fixture
def medical_record2(patient2):
    return MedicalRecord.objects.create(
        patient=patient2,
        medical_condition='HE',
        medical_record=SimpleUploadedFile('test_record2.txt', b'medical_record2', content_type='text/plain')
    )
