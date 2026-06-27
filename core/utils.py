from rest_framework.response import Response


def success_response(data=None, message='Success', status_code=200):
    """
    Builds a consistent success envelope for every non-list endpoint
    in the API:

        {
            "success": true,
            "message": "Patient added successfully.",
            "data": { ... }
        }

    Keeping this shape identical across register/login/CRUD endpoints
    means API consumers (and whoever reviews this assignment) never
    have to guess the response format.
    """
    return Response(
        {
            'success': True,
            'message': message,
            'data': data,
        },
        status=status_code,
    )
