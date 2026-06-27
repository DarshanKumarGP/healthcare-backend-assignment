from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from core.utils import success_response
from patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import MappingSerializer, PatientMappingsSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    """
    POST /api/mappings/ -- Assign a doctor to a patient.
    GET  /api/mappings/ -- Retrieve all patient-doctor mappings
                            created by the authenticated user.
    """

    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save(created_by=request.user)
        return success_response(
            data=self.get_serializer(mapping).data,
            message='Doctor assigned to patient successfully.',
            status_code=status.HTTP_201_CREATED,
        )


class MappingDetailView(APIView):
    """
    GET    /api/mappings/<id>/ -- Get all doctors assigned to the patient with this id.
    DELETE /api/mappings/<id>/ -- Remove the doctor-patient mapping with this id.

    Design note: the assignment spec lists these as two separate
    endpoints that happen to share the exact same URL shape
    (/api/mappings/<id>/) but with different semantics for <id> --
    a patient id on GET, a mapping id on DELETE. Rather than bolt on
    an inconsistent extra path segment, this single view honors the
    literal URL contract from the spec and dispatches by HTTP method,
    which is exactly what GET vs DELETE on one resource path is meant
    to express in REST.

    Both operations are scoped to the requesting user's own data, so
    a user can never view or delete mappings/patients they don't own.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        patient = get_object_or_404(Patient, pk=id, created_by=request.user)
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        serializer = PatientMappingsSerializer(mappings, many=True)
        return success_response(
            data=serializer.data,
            message=f'Doctors assigned to patient "{patient.name}" retrieved successfully.',
        )

    def delete(self, request, id):
        mapping = get_object_or_404(PatientDoctorMapping, pk=id, created_by=request.user)
        mapping.delete()
        return success_response(message='Mapping deleted successfully.')
