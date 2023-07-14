from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from api.models import Collection, PromptTemplate, LLM


class ExampleTest(TestCase):
    """Here you explain the overall functionality you are testing."""

    def setUp(self):
        self.reusable_element = True

    def test_testing(self):
        """Here you explain what the purpose of this test is."""
        self.assertTrue(self.reusable_element)


class TestCollectionModel(TestCase):
    """Test collection model class."""

    def setUp(self):
        self.collection = Collection(name="test", file_path="path/path")
        self.prompt_template1 = PromptTemplate(name="test1",
                                               instruction="test_instruction",
                                               question_format=r"{context}",
                                               answer_format=r"{answer}")
        self.prompt_template2 = PromptTemplate(name="test2",
                                               instruction="test_instruction",
                                               question_format=r"{question}",
                                               answer_format=r"{answer}")
        self.prompt_template3 = PromptTemplate(name="test3",
                                               instruction="test_instruction",
                                               question_format=r"{question}{context}",
                                               answer_format=r"nothing")

    def test_instantiation(self):
        """Test that model instantiates properly."""
        self.assertIsNotNone(self.collection)

    def test_chunk_validation(self):
        """Test that chunk overlap cannot be more than chunk size."""
        collection = self.collection
        collection.chunk_size = 100
        collection.chunk_overlap = 200

        with self.assertRaises(ValidationError):
            collection.full_clean()

    def test_prompt_validation(self):
        """
        Test that prompt_template question format must contain {question} and {context}.
        Test that prompt_template answer format must contain {answer}.
        """
        prompt_template1 = self.prompt_template1
        prompt_template2 = self.prompt_template2
        prompt_template3 = self.prompt_template3

        with self.assertRaises(ValidationError):
            prompt_template1.full_clean()

        with self.assertRaises(ValidationError):
            prompt_template2.full_clean()

        with self.assertRaises(ValidationError):
            prompt_template3.full_clean()

class TestPromptTemplate(TestCase):
    """Test prompt template model class."""

    def setUp(self):
        self.correct_template = "This is a test prompt instruction."
        self.prompt_template = PromptTemplate(name="test",
                                              instruction="test_instruction",
                                              question_format=r"{context}{question}",
                                              answer_format=r"{answer}")
        self.prompt_template_active = PromptTemplate(name="test",
                                                     instruction="test_instruction",
                                                     question_format=r"{context}{question}",
                                                     answer_format=r"{answer}")
        self.correct_instruction = "This is a test prompt instruction."

    def test_instantiation(self):
        """Test that model instantiates properly."""
        self.assertIsNotNone(self.prompt_template)

    def test_active_prompt(self):
        """Test that there can only be one active prompt."""
        prompt1 = self.prompt_template
        prompt2 = self.prompt_template_active
        prompt1.active = True
        prompt1.instruction = self.correct_template
        prompt2.instruction = self.correct_template
        prompt1.save()

        with self.assertRaises(IntegrityError):
            prompt2.save()


class TestLLM(TestCase):
    """Test LLM model class."""

    def setUp(self):
        self.model_inactive = LLM(name="model1", active=False)
        self.model_active = LLM(name="model2", active=True)

    def test_instantiation(self):
        """Test that model instantiates properly."""
        self.assertIsNotNone(self.model_active)

    def test_active_llm(self):
        """Test that there can only be one active model."""
        model1 = self.model_active
        model2 = self.model_inactive
        model2.active = True
        model1.save()

        with self.assertRaises(IntegrityError):
            model2.save()
