from rest_framework import generics, permissions, status

from core.permissions import IsOwnerForWriteElseAuthenticated
from core.utils import success_response

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    POST /api/doctors/ -- Add a new doctor (authenticated users only).
    GET  /api/doctors/ -- Retrieve all doctors (shared across all users).
    """

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = serializer.save(created_by=request.user)
        return success_response(
            data=self.get_serializer(doctor).data,
            message='Doctor added successfully.',
            status_code=status.HTTP_201_CREATED,
        )


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/doctors/<id>/ -- Get details of a specific doctor (any authenticated user).
    PUT    /api/doctors/<id>/ -- Update doctor details (creator only).
    DELETE /api/doctors/<id>/ -- Delete a doctor record (creator only).
    """

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerForWriteElseAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message='Doctor retrieved successfully.')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response(data=serializer.data, message='Doctor updated successfully.')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message='Doctor deleted successfully.')
