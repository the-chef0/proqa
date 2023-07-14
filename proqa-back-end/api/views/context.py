"""
Endpoints that are used to communicate with the VectorDB.
"""
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.utils.context import reset_collection
from api.utils.vectordb import VECTORDB_CLIENT


@api_view(['POST'])
def sources(request) -> Response:
    """
    Endpoint for constructing vector DB from sources directory

        Args:
            request (Request): API request
        Returns:
            Response: "done" if sources were added to DB
    """
    collection_name = request.data['collection_name']
    reset_collection(client=VECTORDB_CLIENT, collection_name=collection_name)

    return Response("done")
