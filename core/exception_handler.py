from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default exception handler so every error response
    (validation errors, 401/403/404, throttling, etc.) shares one
    consistent shape across the whole API:

        {
            "success": false,
            "message": "<human readable summary>",
            "errors": <field-level detail / raw DRF error payload>
        }

    This satisfies the assignment's "implement error handling and
    validation" requirement project-wide instead of repeating
    try/except blocks in every view.
    """
    response = exception_handler(exc, context)

    if response is None:
        # An unhandled, unexpected exception (e.g. a bug or a DB
        # connection error). Never leak internals to the client in
        # production; only show details when DEBUG is on.
        return Response(
            {
                'success': False,
                'message': 'An unexpected error occurred. Please try again later.',
                'errors': str(exc) if settings.DEBUG else None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    message = 'Request failed.'
    if isinstance(response.data, dict) and 'detail' in response.data:
        message = str(response.data['detail'])

    response.data = {
        'success': False,
        'message': message,
        'errors': response.data,
    }
    return response
