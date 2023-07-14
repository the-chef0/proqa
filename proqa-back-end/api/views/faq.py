"""
Endpoints that are used to communicate with Postgres (chat sessions).
"""
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.utils.faq import get_faq_entries


@api_view(['POST'])
def faq_entries(request) -> Response:
    """
    Endpoint for getting FAQ entries.

        Args:
            request (Request): API request, with number of faq entries to return at most
        Returns:
            Response: FAQ entries in JSON format containing id and question
    """
    # Get number of entries to return
    number_of_faq_entries = int(request.data['number'])

    # Get FAQ entries
    faq_entry_list = get_faq_entries(number_of_faq_entries)

    # Return FAQ entries
    return Response({"faq_entries": faq_entry_list})
