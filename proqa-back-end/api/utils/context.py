"""
Helper functions for making API calls to vector DB
"""
import sys
import datetime
from os import listdir
from os.path import isfile, join
from random import randrange
from uuid import uuid4
from typing import Tuple
import filetype
from django.conf import settings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.conversions.common_types import ScoredPoint
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.document_loaders.base import BaseLoader
from langchain.text_splitter import CharacterTextSplitter
from api.utils.aiservice_embedding import EmbeddingAdapter
from api.models import Collection, Source, Chunk, SupportedFiletypes
from api.exceptions import UnsupportedFileTypeException


def vector_db_query(client: QdrantClient, embedding: list) -> ScoredPoint:
    """
    Gets top search result from vector DB based on embedding

        Args:
            client (QdrantClient): Connection to vector DB
            embedding (list): Embedding that is being queried
        Returns:
            ScoredPoint: Top Qdrant search result
    """
    collections = Collection.objects.filter(active=True)
    if not collections.exists():
        raise Collection.DoesNotExist('No active collections in database.')

    max_score_hit = None
    for collection in collections:
        curr_collection_hit = client.search(
            collection_name=collection.name,
            query_vector=embedding,
            limit=1
        )[0]
        if max_score_hit:  # Not equal to None
            if curr_collection_hit.score > max_score_hit.score:
                max_score_hit = curr_collection_hit
        else:
            max_score_hit = curr_collection_hit

    return max_score_hit


def get_context_uuid(client: QdrantClient, embedding: list) -> uuid4:
    """
    Extracts context UUID from vector DB search resuilt

        Args:
            client (QdrantClient): Connection to vector DB
            embedding (list): Embedding that is being queried
        Returns:
            uuid4: top search result UUID
    """
    return vector_db_query(client, embedding).payload['uuid']


def handle_inactive_collection(client: QdrantClient, collection: Collection):
    """
    Deletes inactive collection from local DB and vector DB
    """
    collection.delete()
    client.delete_collection(collection_name=collection.name)


def reset_collection(client: QdrantClient, collection_name: str):
    """
    Creates collection in vector DB with files in the directory
    specified in the instance of the Collection model with name
    collection_name. Assumes that such an entry exists in the database.

        Args:
            client (QdrantClient): Connection to vector DB
            collection_name (str): Name of an existing Collection in the DB
    """
    collection = Collection.objects.get(name=collection_name)
    if not collection.active and not collection.updating:
        handle_inactive_collection(client=client, collection=collection)
        return

    # Delete chunks that are not used by any answer
    Chunk.objects.filter(times_referenced=0).delete()
    # Delete all sources
    collection.source_set.all().delete()
    # Reset collection in the vector DB
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=settings.EMBEDDING_SIZE, distance=Distance.COSINE)
    )
    # Look for files in directory defined in collection
    file_path = collection.file_path
    files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    for file_name in files:
        source_text, source = parse_source(file_path, file_name, collection)
        source.save()
        chunks = parse_chunks(client, source_text, source, collection)
        _ = [chunk.save() for chunk in chunks]
    # Update sources last updated timestamp
    collection.sources_last_updated_at = datetime.datetime.now()
    collection.save(update_fields=["sources_last_updated_at"])


def parse_source(file_path: str, file_name: str, collection: Collection) -> Tuple[str, Source]:
    """
    Given a file defined by file_path and file_name, stores its representation
    in the local database and returns a string representation.

        Args:
            file_path (str): Path to parent dir of file
            file_name (str): Name of the file
            collection (Collection): Parent collection of resulting Source
        Returns:
            str: String representation of file content
            Source: Django model representation of file
    """
    path_to_file = join(file_path, file_name)
    file_type = filetype.guess(path_to_file).EXTENSION
    loader = get_loader_by_file(path_to_file=path_to_file, file_type=file_type)
    # Create source representation
    source = Source(
        collection=collection,
        file_name=file_name,
        file_type=file_type
    )
    # Create string representation of file
    pages = loader.load()
    source_text = ""
    for page in pages:
        source_text += page.page_content
    return source_text, source


def get_loader_by_file(path_to_file: str, file_type: str) -> BaseLoader:
    """
    Creates a concrete instance of the BaseLoader class based on file_type
    """
    if file_type not in SupportedFiletypes.ALL:
        raise UnsupportedFileTypeException
    match file_type:
        case SupportedFiletypes.PDF_EXTENSION:
            return PyPDFLoader(path_to_file)
        case SupportedFiletypes.DOCX_EXTENSION:
            return Docx2txtLoader(path_to_file)


def parse_chunks(client: QdrantClient, source_text: str, source: Source,
                 collection: Collection) -> list[Chunk]:
    """
    Given a source, its text and a collection, creates chunks, stores them
    in the local DB and creates embeddings in the vector DB.

        Args:
            client (QdrantClient): Connection to vector DB
            source_text (str): String representation of source
            source (Source): Django model representation of source
            collection (Collection): Collection that source belongs to
        Returns:
            list: Chunks created from source
    """
    splitter = CharacterTextSplitter(
        chunk_size=collection.chunk_size,
        chunk_overlap=collection.chunk_overlap,
        separator='\n'
    )
    chunks = []
    points = []
    chunks_texts = splitter.split_text(source_text)
    for chunk_text in chunks_texts:
        # Create chunk representation in local DB
        chunk = Chunk(
            source=source,
            content=chunk_text.replace('\x00', ' ')
        )
        chunks.append(chunk)
        # Store embedding in vector DB
        _, vector = EmbeddingAdapter().get(text=chunk_text)
        point = PointStruct(
                    # Irrelevant but required by API
                    id=randrange(sys.maxsize),
                    vector=vector,
                    payload={"uuid": chunk.chunk_id}
                )
        points.append(point)
    client.upsert(collection_name=collection.name, points=points)
    return chunks

def toggle_collection(collection: Collection, state: bool):
    """Toggle the updating state of a collection

        Args:
            collection (Collection): collection to update.
            state (bool): true if the collection is updating.
    """
    collection.updating = state
    collection.save()
