"""
Helper functions for making API calls to Django backend.
"""
import random
from api.models.chat import FAQEntry


def get_faq_entries(number_of_entries: int) -> list:
    """
    Gets at most number_of_faq_entries active random FAQ entries.

        Args:
            number_of_faq_entries (int): Number of entries to return at most
        Returns:
            list: FAQ entries in JSON format
    """

    # Get active entries from FAQEntry table
    faq_entries = FAQEntry.objects.filter(is_active=True)

    # Get number_of_faq_entries random entries from faq_entries (without repetition)
    random_faq_entries = random.sample(list(faq_entries), min(number_of_entries, len(faq_entries)))

    # Create list of FAQ entries in JSON format
    faq_entry_list = []

    for entry in random_faq_entries:
        entry_json = {
            "id": entry.faq_id,
            "question": entry.question,
            "answer": entry.answer,
        }

        faq_entry_list.append(entry_json)

    # Return list of FAQ entries in JSON format
    return faq_entry_list
