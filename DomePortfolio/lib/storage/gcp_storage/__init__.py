from .storage import GCPStorage
from django.conf import settings


class ImageStorage(GCPStorage):
    bucket_name = settings.GCP_BUCKETS.get("images")


class FileStorage(GCPStorage):
    bucket_name = settings.GCP_BUCKETS.get("files")

    def get_valid_name(self, name: str) -> str:
        return name


__all__ = ["GCPStorage", "ImageStorage", "FileStorage"]
