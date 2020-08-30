from decimal import Decimal, ROUND_HALF_EVEN

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from DomePortfolio.lib.payments.paypal import PayPalClient
from .models import models
from ..orders.models import Order
from .models import serializers


class ShopViewset(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.ShopItemSerializer
    queryset = models.Item.objects.all()

    @action(detail=True, methods=["get"], name="Create Payment")
    def payment(self, request, pk: str):
        """Create a PayPal payment from a shop item"""
        obj = get_object_or_404(self.queryset, pk=pk)

        # PayPal expects a value with 2-digits precision,
        # so we round it down from the internal precision of 4-digits
        price = obj.price.amount
        if price.as_tuple().exponent != -2:
            price = price.quantize(Decimal("0.00"), rounding=ROUND_HALF_EVEN)
        price = str(price)
        currency = obj.price.currency.code

        paypal = PayPalClient(
            sandbox=settings.PAYPAL_SANDBOX,
            client_id=settings.PAYPAL_CLIENT,
            client_secret=settings.PAYPAL_SECRET,
        )
        order = Order.objects.create(
            product=obj,
            amount=price,
            purchased_with_sale=obj.sale
        )
        res = paypal.create_payment(
            price=price, reference=str(order.pk), currency=currency
        )
        order.related_paypal_order = res.result.id
        order.save()
        return Response({
            "order": str(order.pk),
        }, 201)
