from django.core.validators import MaxValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from imagekit.models import ProcessedImageField

from DomePortfolio.lib.images.specs import ImageSpec, ThumbnailSpec
from DomePortfolio.lib.images.types import BaseImage
from DomePortfolio.lib.storage.gcp_storage import ImageStorage, FileStorage
import uuid


class Item(models.Model):
    title = models.CharField(max_length=50)
    thumbnail = ProcessedImageField(spec=ThumbnailSpec, storage=ImageStorage())
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="EUR")
    sale = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )
    description = models.TextField()
    download = models.FileField(storage=FileStorage())

    def __str__(self):
        return self.title


class Image(BaseImage):
    # Representing the "before" image
    image = ProcessedImageField(spec=ImageSpec, storage=ImageStorage())
    # Representing the "after" image
    image_after = ProcessedImageField(spec=ImageSpec, storage=ImageStorage())
    parent_item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        null=True,
        related_name="images"
    )


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        to=Item,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders"
    )
    completed = models.BooleanField(default=False)
    related_paypal_order = models.CharField(max_length=100)

    created_on = models.DateTimeField(auto_now_add=True)
    ordered_on = models.DateTimeField(null=True)

    customer_email = models.EmailField(null=True)
    customer_id = models.CharField(max_length=100, null=True)

    amount = MoneyField(
        max_digits=19, decimal_places=4, default_currency="EUR"
    )
    purchased_with_sale = models.PositiveSmallIntegerField(default=0)

    product_downloads_remaining = models.PositiveSmallIntegerField(null=True)
    download_expires_on = models.DateTimeField(null=True)
    product_download = models.URLField(null=True)

    def __str__(self) -> str:
        return f"Order for Item {self.product.pk}; {self.product.title}"


__all__ = ["Item", "Image", "Order"]
