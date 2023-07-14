import uuid

from django.core.exceptions import ValidationError
from django.db import models

from api.models.abstract import Rateable
from api.models.choices import SUPPORTED_FILETYPES


class Collection(models.Model):
    """A collection represents a set of sources."""
    name = models.CharField(max_length=100, unique=True)
    file_path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    updating = models.BooleanField(default=False)
    chunk_size = models.PositiveIntegerField(default=1000)
    chunk_overlap = models.PositiveIntegerField(default=500)
    sources_last_updated_at = models.DateTimeField(null=True)

    def clean(self):
        if self.chunk_overlap >= self.chunk_size:
            raise ValidationError("Chunk overlap cannot be more than chunk size.")

    def __str__(self):
        return f'{self.name}'


class Source(Rateable):
    """Represent a document. Does not store the document itself."""
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(choices=SUPPORTED_FILETYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_upvotes(self):
        """Get total number of upvotes from all answers using this source."""
        return sum(chunk.upvotes for chunk in self.chunk_set.all())

    def get_downvotes(self):
        """Get total number of downvotes from all answers using this source."""
        return sum(chunk.downvotes for chunk in self.chunk_set.all())

    def __str__(self):
        return f'{self.file_name}'

    class Meta:
        # A collection can only have one instance of the same document.
        constraints = [
            models.UniqueConstraint(
                fields=['collection', 'file_name'], name='unique_document')
        ]


class Chunk(Rateable):
    """A source is divided into smaller chunks."""
    chunk_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    times_referenced = models.IntegerField(default=0)

    def get_upvotes(self):
        """Get total number of upvotes from all answers using this chunk."""
        if self.answer_set.exists():
            return self.answer_set.filter(rating=1).count()
        return 0

    def get_downvotes(self):
        """Get total number of downvotes from all answers using this chunk."""
        if self.answer_set.exists():
            return self.answer_set.filter(rating=-1).count()
        return 0

    def __str__(self):
        return f'{self.source}:{self.chunk_id}'
