from django.contrib.admin import TabularInline, ModelAdmin, action
from django.contrib import messages

from api.models import Source, Chunk
from api.tasks import update_collections
from api.utils.context import toggle_collection


class SourceInline(TabularInline):
    """Inline model for sources in a collection."""
    extra = 0
    model = Source
    readonly_fields = ["file_name", "file_type"]


class CollectionAdmin(ModelAdmin):
    """Model admin for collection model."""
    inlines = [SourceInline]
    readonly_fields = ["sources_last_updated_at", "updating"]
    actions = ["update_sources"]
    list_display = ["name", "active", "updating"]

    @action(description="Update sources in selected collections")
    def update_sources(self, request, queryset):
        """Updates sources in selected collections.
           Calls the update_collections task.
        """
        queue = []
        for collection in queryset:
            if not collection.updating:
                toggle_collection(collection, True)
                queue.append(collection.name)

        update_collections.delay(queue)
        messages.success(request, f"{len(queue)} sources scheduled for update.")


class ChunkInline(TabularInline):
    """Inline model for chunks in a source."""
    extra = 0
    model = Chunk
    readonly_fields = ["content"]

class ChunkAdmin(ModelAdmin):
    """
    Model admin for chunk model.
    """
    readonly_fields = ["times_referenced"]


class SourceAdmin(ModelAdmin):
    """Model admin for source model."""
    readonly_fields = ["collection", "file_name", "file_type", "upvotes", "downvotes"]
    inlines = [ChunkInline]
