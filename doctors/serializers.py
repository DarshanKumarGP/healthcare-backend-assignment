from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Doctor
        fields = (
            'id', 'name', 'specialization', 'age', 'gender',
            'email', 'phone_number',
            'created_by', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Name cannot be empty.')
        return value.strip()

    def validate_specialization(self, value):
        if not value.strip():
            raise serializers.ValidationError('Specialization cannot be empty.')
        return value.strip()
