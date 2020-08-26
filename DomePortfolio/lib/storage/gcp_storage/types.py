import mimetypes
from typing import Optional

from django.core.files.base import File
from django.utils.encoding import force_bytes
from google.cloud.storage import Blob
from tempfile import SpooledTemporaryFile


class GCPBlob(File):
    def __init__(  # noqa missed call to super
            self, file: Blob,
            name: Optional[str] = None,
            mode: Optional[str] = "rb"
    ) -> None:
        self.name = name or file.name
        self.mime_type = mimetypes.guess_type(self.name)[0]
        self.blob = file
        self._mode = mode
        self._file = None
        self._is_dirty = False

    @property
    def size(self) -> int:
        return self.blob.size

    def _get_file(self) -> SpooledTemporaryFile:
        if self._file is None:
            self._file = SpooledTemporaryFile(
                suffix=".GCPStorageFile",
            )
            if 'r' in self._mode:
                self._is_dirty = False
                self.blob.download_to_file(self._file)
                self._file.seek(0)
        return self._file

    def _set_file(self, value):
        self._file = value

    file = property(_get_file, _set_file)

    def read(self, num_bytes=None):
        if 'r' not in self._mode:
            raise AttributeError("File was not opened in read mode.")

        if num_bytes is None:
            num_bytes = -1

        return super().read(num_bytes)

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was not opened in write mode.")
        self._is_dirty = True
        return super().write(force_bytes(content))

    def close(self) -> None:
        if self._file is not None:
            if self._is_dirty:
                self.blob.upload_from_file(
                    self.file,
                    rewind=True,
                    content_type=self.mime_type
                )
            self._file.close()
            self._file = None
