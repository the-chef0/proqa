"""
Test cases for api/utils/chat_session.py
"""
from django.test import TestCase
from api.models import FAQEntry
from api.utils.faq import (
    get_faq_entries
)


class TesTFAQ(TestCase):
    """Test cases for faq."""

    def setUp(self):
        """
        Setup reusable elements for tests.
        """
        self.faq_entry_1 = FAQEntry.objects.create(question="testquestion1", answer="testanswer1")
        self.faq_entry_2 = FAQEntry.objects.create(question="testquestion2", answer="testanswer2")

    def test_getting_faq_entries(self):
        """
        Tests that the correct number of FAQ entries are returned.
        """
        # Get 0 entries
        faq_entries = get_faq_entries(0)
        self.assertEqual(len(faq_entries), 0)

        # Get 2
        faq_entries = get_faq_entries(2)
        self.assertEqual(len(faq_entries), 2)

        # Get 3
        faq_entries = get_faq_entries(3)
        self.assertEqual(len(faq_entries), 2)
