"""
Custom exceptions
"""


class UnsupportedFileTypeException(Exception):
    """
    Raised when an attempt is made to load an unsupported file type
    into the databases.
    """
