from django.core.validators import MaxValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from imagekit.models import ProcessedImageField

from DomePortfolio.lib.images.specs import ThumbnailSpec, ShopImageSpec
from DomePortfolio.lib.images.types import BaseImage
from DomePortfolio.lib.storage.gcp_storage import ImageStorage, FileStorage


class Item(models.Model):
    title = models.CharField(max_length=50)
    thumbnail = ProcessedImageField(spec=ThumbnailSpec, storage=ImageStorage())
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="EUR")
    sale = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )
    description = models.TextField(null=True)
    download = models.FileField(storage=FileStorage())

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title


class Image(BaseImage):
    # Representing the "before" image
    image = ProcessedImageField(spec=ShopImageSpec, storage=ImageStorage())
    # Representing the "after" image
    image_after = ProcessedImageField(spec=ShopImageSpec, storage=ImageStorage())
    parent_item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        null=True,
        related_name="images"
    )


__all__ = ["Item", "Image"]
