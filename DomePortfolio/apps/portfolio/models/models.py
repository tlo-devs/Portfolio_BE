from django.db import models
from imagekit.models import ProcessedImageField
from DomePortfolio.lib.images.types import BaseImage
from DomePortfolio.lib.images.specs import ImageSpec, ThumbnailSpec
from DomePortfolio.lib.storage.gcp_storage import GCPStorage
from datetime import datetime


class BaseItem(models.Model):
    title = models.CharField(max_length=30)
    thumbnail = ProcessedImageField(spec=ThumbnailSpec, storage=GCPStorage())
    category = models.ForeignKey(
        to="categories.CategoryTree",
        on_delete=models.SET_NULL,
        null=True
    )
    year = models.PositiveSmallIntegerField(default=datetime.now().year)
    client = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class ImageItem(BaseItem):
    """
    Since the image relationship is a many to one rel.,
    we place the FK on the image table, instead of here.

    We can do a reverse foreign key lookup to the image table,
    via the self.image_set Manager, e.g. with self.image_set.all().
    """
    pass


class VideoItem(BaseItem):
    video = models.URLField()


class Image(BaseImage):
    image = ProcessedImageField(spec=ImageSpec, storage=GCPStorage())
    parent_item = models.ForeignKey(
        to=ImageItem,
        on_delete=models.CASCADE,
        null=True,
        related_name="images"
    )


__all__ = ["ImageItem", "VideoItem", "Image"]
