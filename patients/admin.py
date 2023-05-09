from django.contrib import admin
from .models import Patient, MedicalRecord
from doctors.models import MedicalProfessional


# class AccessControlInline(admin.TabularInline):
#     model = AccessControl
#     extra = 0


class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medical_condition', 'created_at')
    search_fields = ('patient__name', 'medical_condition')
    list_filter = ('created_at', )
    date_hierarchy = 'created_at'


class PatientAdmin(admin.ModelAdmin):
    # inlines = (AccessControlInline, )
    list_display = ('name', 'date_of_birth', 'created_at', '__str__')
    search_fields = ('name', 'date_of_birth')


class MedicalProfessionalAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


admin.site.register(Patient, PatientAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(MedicalProfessional, MedicalProfessionalAdmin)

