from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from imagekit.models import ProcessedImageField

from DomePortfolio.lib.images.specs import ThumbnailSpec, ShopImageSpec
from DomePortfolio.lib.images.types import BaseImage
from DomePortfolio.lib.storage.gcp_storage import ImageStorage, FileStorage


class Download(models.Model):
    file = models.FileField(storage=FileStorage())


@receiver(post_delete, sender=Download)
def delete_remote_file(sender, instance, **kwargs) -> None:
    uri = instance.image.name
    if "/" in uri:
        uri = uri.split("/")[-1]
    storage = instance.image.storage
    storage.delete(uri)


class Item(models.Model):
    title = models.CharField(max_length=50)
    thumbnail = ProcessedImageField(spec=ThumbnailSpec, storage=ImageStorage())
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="EUR")
    sale = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )
    category = models.ForeignKey(
        to="categories.CategoryTree",
        on_delete=models.SET_NULL,
        null=True
    )
    description = models.TextField(null=True)
    download = models.ForeignKey(
        to=Download,
        on_delete=models.CASCADE
    )

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
