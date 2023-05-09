from rest_framework import serializers
from django.contrib.auth.models import User

from .models import MedicalProfessional


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('id', 'date_joined', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}
        exclude = ('groups', 'user_permissions')


class DoctorSerializer(serializers.Serializer):
    user = serializers.IntegerField()

    def validate(self, data):
        if not User.objects.filter(pk=data['user']).exists():
            raise serializers.ValidationError('User does not exist')
        return data

    def create(self, validated_data):
        return MedicalProfessional.objects.create(user=User.objects.get(pk=validated_data['user']))

    def save(self, **kwargs):
        return self.create(self.validated_data)


class DoctorGetSerializer(serializers.Serializer):
    user = UserSerializer()
