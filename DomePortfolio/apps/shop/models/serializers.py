from rest_framework import serializers
from decimal import Decimal
from . import models
from decimal import ROUND_HALF_EVEN


class ShopImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Image

    def to_representation(self, instance):
        return {
            "image_before": instance.image.name,
            "image_after": instance.image_after.name
        }


class PriceSerializer(serializers.Serializer):  # noqa must implement abstract
    base_price = serializers.DecimalField(
        max_digits=19,
        decimal_places=2,
        rounding=ROUND_HALF_EVEN,
        source="price.amount",
        coerce_to_string=False
    )
    current_price = serializers.SerializerMethodField()
    currency = serializers.CharField(source="price.currency")
    sale = serializers.IntegerField()

    # noinspection PyMethodMayBeStatic
    def get_current_price(self, obj):
        sale_percent = Decimal(obj.sale / 100)
        off = obj.price.amount * sale_percent
        return Decimal(
            obj.price.amount - off
        ).quantize(Decimal("0.00"), rounding=ROUND_HALF_EVEN)


class ShopItemSerializer(serializers.ModelSerializer):
    images = ShopImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.Item
        exclude = ("price", "price_currency", "sale", "download")

    def to_representation(self, instance):
        data = super(ShopItemSerializer, self).to_representation(instance)
        data["thumbnail"] = instance.thumbnail.name
        data["price"] = PriceSerializer(instance).data
        return data


class CreateOrderResponseSerializer(serializers.Serializer):  # noqa must implement abstract
    system_order_id = serializers.CharField()
    paypal_order_id = serializers.CharField()
