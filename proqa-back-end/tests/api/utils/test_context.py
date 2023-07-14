"""
Test cases for api/utils/context.py
"""
from os.path import join
from django.test import TestCase
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from api.models import Collection, Source, Chunk
from api.utils.context import (
    vector_db_query,
    get_context_uuid,
    parse_source,
    get_loader_by_file
)
from api.exceptions import UnsupportedFileTypeException
from tests.api.resources import constants as c


class TestContextUtils(TestCase):
    """
    Test cases for api/utils/context.py
    """

    def setUp(self):
        self.test_collection_name = c.TEST_COLLECTION_NAME
        self.test_collection = Collection.objects.create(
            name=self.test_collection_name,
            file_path=c.TEST_FILE_PATH,
            chunk_overlap=50
        )

        self.test_source = Source.objects.create(
            collection=self.test_collection,
            file_name=c.TEST_SOURCE_FILENAME_A,
            file_type="pdf"
        )

        self.test_chunk_a = Chunk.objects.create(
            source=self.test_source,
            content=c.TEST_TEXT_A
        )

        self.test_chunk_b = Chunk.objects.create(
            source=self.test_source,
            content=c.TEST_TEXT_B
        )

        self.test_client = QdrantClient(":memory:")
        self.test_client.recreate_collection(
            collection_name=self.test_collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

        self.test_client.upsert(
            collection_name=self.test_collection_name,
            points=[
                PointStruct(
                    id=0,  # Irrelevant but required by API
                    vector=c.TEST_VECTOR_A,
                    payload={"uuid": self.test_chunk_a.chunk_id}
                )
            ]
        )

        self.test_client.upsert(
            collection_name=self.test_collection_name,
            points=[
                PointStruct(
                    id=1,  # Irrelevant but required by API
                    vector=c.TEST_VECTOR_B,
                    payload={"uuid": self.test_chunk_b.chunk_id}
                )
            ]
        )

    def test_vector_db_query(self):
        """
        Tests vector_db_query.
        """
        hit = vector_db_query(
            client=self.test_client,
            embedding=c.TEST_VECTOR_A
        )
        self.assertEqual(hit.payload['uuid'], self.test_chunk_a.chunk_id)

    def test_get_context_uuid(self):
        """
        Tests get_context_uuid.
        """
        uuid = get_context_uuid(client=self.test_client, embedding=c.TEST_VECTOR_A)
        self.assertEqual(uuid, self.test_chunk_a.chunk_id)

    def test_vector_db_query_no_col(self):
        """
        Tests vector_db_query with empty collections.
        """
        self.test_collection.delete()
        with self.assertRaises(Collection.DoesNotExist):
            vector_db_query(
                    client=self.test_client,
                    embedding=c.TEST_VECTOR_A
            )

    def test_get_context_uuid_no_col(self):
        """
        Tests get_context_uuid with empty collections.
        """
        self.test_collection.delete()
        with self.assertRaises(Collection.DoesNotExist):
            get_context_uuid(client=self.test_client, embedding=c.TEST_VECTOR_A)

    def test_parse_source(self):
        """
        Tests parse_source
        """
        file_name = c.TEST_SOURCE_FILENAME_A
        source_text, source = parse_source(
            file_path=self.test_collection.file_path,
            file_name=file_name,
            collection=self.test_collection
        )
        self.assertEqual(source_text, c.TEST_SOURCE_TEXT)
        self.assertEqual(source.collection, self.test_collection)
        self.assertEqual(source.file_name, file_name)
        self.assertEqual(source.file_type, "pdf")

    def test_get_loader_by_file_pdf(self):
        """
        Tests get_loader_by_file with a PDF file
        """
        path_to_file = join(self.test_collection.file_path, c.TEST_SOURCE_FILENAME_A)
        loader = get_loader_by_file(path_to_file, 'pdf')
        self.assertTrue(isinstance(loader, PyPDFLoader))

    def test_get_loader_by_file_docx(self):
        """
        Tests get_loader_by_file with a DOCX file
        """
        path_to_file = join(self.test_collection.file_path, c.TEST_SOURCE_FILENAME_B)
        loader = get_loader_by_file(path_to_file, 'docx')
        self.assertTrue(isinstance(loader, Docx2txtLoader))

    def test_get_loader_by_file_unsupported(self):
        """
        Tests get_loader_by_file with an unsupported file type
        """
        with self.assertRaises(UnsupportedFileTypeException):
            get_loader_by_file('', 'exe')
