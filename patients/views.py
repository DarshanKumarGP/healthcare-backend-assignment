from rest_framework import generics, permissions, status

from core.permissions import IsOwner
from core.utils import success_response

from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    """
    POST /api/patients/  -- Add a new patient (authenticated users only).
    GET  /api/patients/  -- Retrieve all patients created by the authenticated user.
    """

    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save(created_by=request.user)
        return success_response(
            data=self.get_serializer(patient).data,
            message='Patient added successfully.',
            status_code=status.HTTP_201_CREATED,
        )


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/patients/<id>/ -- Get details of a specific patient.
    PUT    /api/patients/<id>/ -- Update patient details.
    DELETE /api/patients/<id>/ -- Delete a patient record.

    A patient can only be viewed, updated, or deleted by the user who
    created it -- enforced both by scoping the queryset to the
    requesting user AND by the IsOwner object permission (defense in
    depth: even if the queryset filter were ever loosened, the
    permission check still blocks cross-user access).
    """

    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message='Patient retrieved successfully.')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response(data=serializer.data, message='Patient updated successfully.')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message='Patient deleted successfully.')
