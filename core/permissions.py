from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Object-level permission that only allows the user who created
    an object (via its `created_by` field) to view, update, or delete it.

    Used by the Patient resource: patients are private to the user
    who added them.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by_id == request.user.id


class IsOwnerForWriteElseAuthenticated(BasePermission):
    """
    Allows any authenticated user to safely read (GET/HEAD/OPTIONS) an
    object, but only the user who created it can modify (PUT/PATCH) or
    delete it.

    Used by the Doctor resource: doctors are shared/readable by every
    authenticated user, but only their creator can edit or remove them.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by_id == request.user.id
