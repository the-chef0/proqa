from celery import shared_task
from api.models import Collection
from api.utils.context import reset_collection, toggle_collection
from api.utils.vectordb import VECTORDB_CLIENT

@shared_task()
def update_collections(collections: str):
    """Update set of collections using celery.

        Args:
            collections (list): list of collection names.
    """
    for collection in collections:
        update_collection.delay(collection)

@shared_task()
def update_collection(collection: str):
    """Update a collection using celery.

        Args:
            collection (str): name of collection to update.
    """
    coll = Collection.objects.get(name=collection)
    reset_collection(client=VECTORDB_CLIENT, collection_name=collection)
    toggle_collection(coll, False)
