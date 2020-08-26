from random import choices
from string import ascii_letters, digits
from typing import ClassVar

from django.core.files import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from google.cloud import exceptions

from .backend import GCPStorageAdapter
from .types import GCPBlob


@deconstructible
class GCPStorage(Storage):
    backend: ClassVar[GCPStorageAdapter] = GCPStorageAdapter()

    def get_valid_name(self, name: str) -> str:
        *_, ext = name.split(".")
        return f"{''.join(choices(ascii_letters + digits, k=16))}.{ext.lower()}"

    def _open(self, name: str, mode: str = "rb") -> GCPBlob:  # noqa
        file = GCPBlob(
            self.backend.bucket.get_blob(name.split("/")[-1]),
            mode=mode
        )
        if not file:
            raise FileNotFoundError
        return file

    def _save(self, name: str, content: File) -> str:
        dest_blob = self.backend.bucket.blob(name)
        dest_blob.content_type = "image/png"
        dest_blob.upload_from_file(content)
        return dest_blob.public_url

    def delete(self, uri: str) -> bool:
        bucket = self.backend.bucket
        try:
            bucket.delete_blob(uri)
            return True
        except exceptions.NotFound:
            return False

    def exists(self, uri: str) -> bool:
        bucket = self.backend.bucket
        return False if bucket.get_blob(uri) is None else True

    def url(self, name: str) -> str:
        return self.backend.bucket.get_blob(name).public_url

    def size(self, name: str) -> int:
        return self.backend.bucket.get_blob(name).size

    def path(self, *args) -> None:
        """
        Not implemented as the file is not on the local filesystem.
        """
        pass

    def listdir(self, *args) -> None:
        """
        Not implemented because it is not required.
        """
        pass

    def get_accessed_time(self, *args) -> None:
        """
        Not implemented because it is not required.
        """
        pass

    def get_created_time(self, *args) -> None:
        """
        Not implemented because it is not required.
        """
        pass

    def get_modified_time(self, *args) -> None:
        """
        Not implemented because it is not required.
        """
        pass
