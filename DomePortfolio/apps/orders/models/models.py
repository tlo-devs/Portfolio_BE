from django.db import models
import uuid
from djmoney.forms import MoneyField


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        to="shop.Item",
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
