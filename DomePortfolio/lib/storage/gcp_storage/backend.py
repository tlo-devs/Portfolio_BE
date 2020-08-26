from pathlib import Path
from typing import ClassVar, Any

from django.conf import settings
from google.cloud import storage, exceptions
from google.cloud.storage import Bucket


class GCPStorageAdapter:
    __mixin_state: ClassVar["GCPStorageAdapter"] = None
    gcloud_client: ClassVar = storage.Client.from_service_account_json(
        Path(__file__).parent.parent.parent.parent.parent / "keys" / "CLOUD_STORAGE_OPERATOR.json"
    )

    bucket: ClassVar[Bucket] = None

    def __new__(cls) -> "GCPStorageAdapter":
        if not cls.__mixin_state or cls.__mixin_state is None:
            cls.__mixin_state = super().__new__(cls)
            cls.__mixin_state.ready()
        return cls.__mixin_state

    def ready(self) -> None:
        project_name = settings.BASE_DIR.split("/")[-1:][0]
        bucket_name = f"{project_name}-IMAGE-BUCKET".lower()
        try:
            # In case the bucket has not been set up with Terraform we create it
            self.bucket = self.gcloud_client.create_bucket(
                bucket_name, location="EUROPE-WEST3"
            )
        except exceptions.Conflict:
            self.bucket = self.gcloud_client.get_bucket(bucket_name)
        self.bucket.make_public(future=True)

    def __delattr__(self, item: Any) -> None:
        raise ValueError("Values are immutable.")
