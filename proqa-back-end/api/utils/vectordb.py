from django.conf import settings
from qdrant_client import QdrantClient

# Creates a QdrantClient instance
VECTORDB_CLIENT = QdrantClient(url=settings.QDRANT_URL)
