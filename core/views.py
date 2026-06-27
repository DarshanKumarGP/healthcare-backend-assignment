from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from core.utils import success_response


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """GET /api/health/ -- lightweight endpoint to confirm the API is up."""
    return success_response(
        data={'status': 'ok'},
        message='Healthcare Backend API is running.',
    )
