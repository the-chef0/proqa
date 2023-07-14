from abc import ABCMeta, abstractmethod

from django.db import models


class AbstractModelMeta(ABCMeta, type(models.Model)):
    """Abstract class meta for django models."""


class Rateable(models.Model, metaclass=AbstractModelMeta):
    """Abstract rateable model with upvotes and downvotes."""

    @property
    def upvotes(self):
        """Upvote property calculated on viewing."""
        return self.get_upvotes()

    @property
    def downvotes(self):
        """Downvote property calculated on viewing."""
        return self.get_downvotes()

    @abstractmethod
    def get_upvotes(self):
        """Abstract method to get the number of upvotes."""

    @abstractmethod
    def get_downvotes(self):
        """Abstract method to get the number of downvotes."""

    class Meta:
        abstract = True
