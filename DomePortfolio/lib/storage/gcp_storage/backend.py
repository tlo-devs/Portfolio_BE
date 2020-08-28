from pathlib import Path
from typing import ClassVar, Any, Dict

from django.conf import settings
from google.cloud import storage, exceptions
from google.cloud.storage import Bucket

KEYS_FOLDER = Path(__file__).parent.parent.parent.parent.parent / "keys"


class GCPStorageAdapter:
    __mixin_state: ClassVar["GCPStorageAdapter"] = None
    gcloud_client: ClassVar = storage.Client.from_service_account_json(
         KEYS_FOLDER / "CLOUD_STORAGE_OPERATOR.json"
    )

    buckets: ClassVar[Dict[str, Bucket]] = {}

    def __new__(cls) -> "GCPStorageAdapter":
        if not cls.__mixin_state or cls.__mixin_state is None:
            cls.__mixin_state = super().__new__(cls)
            cls.__mixin_state.__init(settings.GCP_BUCKETS)
        return cls.__mixin_state

    def __init(self, buckets: dict) -> None:
        try:
            for key, name in buckets.items():
                self.buckets[name] = self.gcloud_client.get_bucket(name)
        except exceptions.NotFound as e:
            raise e

    def __delattr__(self, item: Any) -> None:
        raise ValueError("Values are immutable.")
