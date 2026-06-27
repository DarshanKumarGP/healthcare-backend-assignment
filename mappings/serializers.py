from rest_framework import serializers

from doctors.serializers import DoctorSerializer

from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):
    """Used for POST/GET on /api/mappings/."""

    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = PatientDoctorMapping
        fields = (
            'id', 'patient', 'doctor', 'patient_name', 'doctor_name',
            'created_by', 'created_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'patient_name', 'doctor_name')

    def validate_patient(self, value):
        request = self.context['request']
        if value.created_by_id != request.user.id:
            raise serializers.ValidationError('You can only map doctors to your own patients.')
        return value

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        if patient and doctor and PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError('This doctor is already assigned to this patient.')
        return attrs


class PatientMappingsSerializer(serializers.ModelSerializer):
    """Used for GET /api/mappings/<patient_id>/ -- lists doctors assigned to one patient."""

    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'doctor', 'created_at')
