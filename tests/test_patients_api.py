import os

import pytest
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from patients.models import MedicalRecord

pytestmark = pytest.mark.django_db


class TestPatientsAPISuccess:
    endpoint = '/api/patients/'

    @pytestmark
    def test_get_patients_success(self, api_client, med_professional1, med_professional2, patient1, patient2):
        api_client.force_authenticate(user=med_professional1.user)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['name'] == patient1.name
        assert response.data[0]['date_of_birth'] == patient1.date_of_birth
        assert response.data[0]['doctors'][0] == med_professional1.id
        assert response.data[1]['name'] == patient2.name
        assert response.data[1]['date_of_birth'] == patient2.date_of_birth
        assert response.data[1]['doctors'][0] == med_professional2.id

    @pytestmark
    def test_get_patient_success(self, api_client, med_professional1, patient1):
        api_client.force_authenticate(user=med_professional1.user)
        response = api_client.get(self.endpoint + str(patient1.id) + '/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == patient1.name
        assert response.data['date_of_birth'] == patient1.date_of_birth
        assert response.data['doctors'][0] == med_professional1.id

    @pytestmark
    def test_create_patient_success(self, api_client, med_professional1, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
            'doctors': [
                med_professional1.id
            ]
        }
        response = api_client.post(self.endpoint, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == data['name']
        assert response.data['date_of_birth'] == data['date_of_birth']
        assert response.data['doctors'][0] == med_professional1.id

    @pytestmark
    def test_create_patient_success_no_doctors(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
        }
        response = api_client.post(self.endpoint, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == data['name']
        assert response.data['date_of_birth'] == data['date_of_birth']
        assert response.data['doctors'] == []

    @pytestmark
    def test_update_patient_success(self, api_client, med_professional1, patient1, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
            'doctors': [
                med_professional1.id
            ]
        }
        response = api_client.put(self.endpoint + str(patient1.id) + '/', data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == data['name']
        assert response.data['date_of_birth'] == data['date_of_birth']
        assert response.data['doctors'][0] == med_professional1.id

    @pytestmark
    def test_partial_update_patient_success(self, api_client, med_professional1, patient1, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            'name': 'test_patient',
        }
        response = api_client.patch(self.endpoint + str(patient1.id) + '/', data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == data['name']
        assert response.data['date_of_birth'] == patient1.date_of_birth
        assert response.data['doctors'][0] == med_professional1.id

    @pytestmark
    def test_delete_patient_success(self, api_client, med_professional1, patient1, admin_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(self.endpoint + str(patient1.id) + '/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not MedicalRecord.objects.filter(id=patient1.id).exists()



class TestPatientsAPIFailure:
    endpoint = '/api/patients/'

    @pytestmark
    def test_get_patients_fail(self, api_client, patient1, patient2):
        """
        This test checks for fail because the user is not authenticated.
        """
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytestmark
    def test_get_patients_fail_non_professional(self, api_client, patient1, patient2, user3):
        """
        This test checks for fail because the user is not a medical professional.
        """
        api_client.force_authenticate(user=user3)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytestmark
    def test_get_patient_fail(self, api_client, patient1):
        """
        This test checks for fail because the user is not authenticated.
        """
        response = api_client.get(self.endpoint + str(patient1.id) + '/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytestmark
    def test_get_patient_fail_non_professional(self, api_client, patient1, user3):
        """
        This test checks for fail because the user is not a medical professional.
        """
        api_client.force_authenticate(user=user3)
        response = api_client.get(self.endpoint + str(patient1.id) + '/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytestmark
    def test_create_patient_fail(self, api_client, med_professional1):
        """
        This test checks for fail because the user is not authenticated.
        """
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
            'doctors': [
                med_professional1.id
            ]
        }
        response = api_client.post(self.endpoint, data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytestmark
    def test_create_patient_fail_non_professional(self, api_client, med_professional1, user3):
        """
        This test checks for fail because the user is not a medical professional.
        """
        api_client.force_authenticate(user=user3)
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
            'doctors': [
                med_professional1.id
            ]
        }
        response = api_client.post(self.endpoint, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytestmark
    def test_create_patient_fail_non_admin(self, api_client, med_professional1, patient1):
        """
        This test checks for fail because the user is not an admin.
        """
        api_client.force_authenticate(user=med_professional1.user)
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
            'doctors': [
                med_professional1.id
            ]
        }
        response = api_client.post(self.endpoint, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytestmark
    def test_update_patient_fail(self, api_client, med_professional1, patient1):
        """
        This test checks for fail because the user is not authenticated.
        """
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
            'doctors': [
                med_professional1.id
            ]
        }
        response = api_client.put(self.endpoint + str(patient1.id) + '/', data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytestmark
    def test_update_patient_fail_non_professional(self, api_client, med_professional1, patient1, user3):
        """
        This test checks for fail because the user is not a medical professional.
        """
        api_client.force_authenticate(user=user3)
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
            'doctors': [
                med_professional1.id
            ]
        }
        response = api_client.put(self.endpoint + str(patient1.id) + '/', data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytestmark
    def test_update_patient_fail_non_admin(self, api_client, med_professional1, patient1):
        """
        This test checks for fail because the user is not an admin.
        """
        api_client.force_authenticate(user=med_professional1.user)
        data = {
            'name': 'test_patient',
            'date_of_birth': '2000-01-01',
            'doctors': [
                med_professional1.id
            ]
        }
        response = api_client.put(self.endpoint + str(patient1.id) + '/', data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytestmark
    def test_delete_patient_fail(self, api_client, med_professional1, patient1):
        """
        This test checks for fail because the user is not authenticated.
        """
        response = api_client.delete(self.endpoint + str(patient1.id) + '/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytestmark
    def test_delete_patient_fail_non_admin(self, api_client, med_professional1, patient1):
        """
        This test checks for fail because the user is not a medical professional.
        """
        api_client.force_authenticate(user=med_professional1.user)
        response = api_client.delete(self.endpoint + str(patient1.id) + '/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestMedicalRecordsAPISuccess:
    endpoint = '/api/medical-records/'

    @pytestmark
    def test_get_medical_records_success(self, api_client, med_professional1, patient1, medical_record1,
                                         medical_record11):
        api_client.force_authenticate(user=med_professional1.user)
        response = api_client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['patient'] == patient1.id
        assert response.data[0]['medical_record'] == 'http://testserver/' + medical_record1.medical_record.name
        assert response.data[0]['medical_condition'] == medical_record1.medical_condition
        assert response.data[1]['patient'] == patient1.id
        assert response.data[1]['medical_record'] == 'http://testserver/' + medical_record11.medical_record.name
        assert response.data[1]['medical_condition'] == medical_record11.medical_condition


    @pytestmark
    def test_get_medical_record_success(self, api_client, med_professional1, patient1, medical_record1):
        api_client.force_authenticate(user=med_professional1.user)
        response = api_client.get(self.endpoint + str(medical_record1.id) + '/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['patient'] == patient1.id
        assert response.data['medical_record'] == 'http://testserver/' + medical_record1.medical_record.name
        assert response.data['medical_condition'] == medical_record1.medical_condition

    @pytestmark
    def test_download_medical_record_file_success(self, api_client, medical_record1, patient1, med_professional1):
        api_client.force_authenticate(user=med_professional1.user)
        response = api_client.get(self.endpoint + str(medical_record1.id) + '/dl_med_record/')
        assert response.status_code == status.HTTP_200_OK
        assert response.content == medical_record1.medical_record.read()


    @pytestmark
    def test_create_medical_record_success(self, api_client, patient1, med_professional1):
        api_client.force_authenticate(user=med_professional1.user)
        data = {
            'patient': patient1.id,
            'medical_condition': 'UH',
            'medical_record': SimpleUploadedFile('test_medical_record.txt', b'file_content', content_type='text/plain')
        }
        response = api_client.post(self.endpoint, data=data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['patient'] == patient1.id
        assert response.data['medical_record'] == 'http://testserver/static/medical_files/' + data[
            'medical_record'].name
        assert response.data['medical_condition'] == data['medical_condition']


    @pytestmark
    def test_update_medical_record_success(self, api_client, medical_record1, patient1, med_professional1):
        api_client.force_authenticate(user=med_professional1.user)
        data = {
            'patient': patient1.id,
            'medical_condition': 'UH',
            'medical_record': SimpleUploadedFile('test_medical_record.txt', b'file_content', content_type='text/plain')
        }
        response = api_client.put(self.endpoint + str(medical_record1.id) + '/', data=data, format='multipart')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['patient'] == patient1.id
        assert response.data['medical_condition'] == data['medical_condition']


    @pytestmark
    def test_partial_update_medical_record_success(self, api_client, medical_record1, patient1, med_professional1):
        api_client.force_authenticate(user=med_professional1.user)
        data = {
            'medical_condition': 'UH',
        }
        response = api_client.patch(self.endpoint + str(medical_record1.id) + '/', data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['patient'] == patient1.id
        assert response.data['medical_record'] == 'http://testserver/' + medical_record1.medical_record.name
        assert response.data['medical_condition'] == data['medical_condition']


    @pytestmark
    def test_delete_medical_record_success(self, api_client, medical_record1, med_professional1):
        api_client.force_authenticate(user=med_professional1.user)
        response = api_client.delete(self.endpoint + str(medical_record1.id) + '/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not MedicalRecord.objects.filter(id=medical_record1.id).exists()
