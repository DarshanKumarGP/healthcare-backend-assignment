from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    """
    Used as the project-wide default pagination class so every "list"
    endpoint (GET /api/patients/, GET /api/doctors/, GET /api/mappings/)
    returns a consistent, predictable JSON envelope:

        {
            "success": true,
            "count": 23,
            "next": "http://.../?page=2",
            "previous": null,
            "results": [ ... ]
        }

    Clients can request a different page size with ?page_size=, up to
    `max_page_size`.
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
