from decimal import Decimal, ROUND_HALF_EVEN

from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from DomePortfolio.lib.payments.paypal import PayPalClient
from .models import models
from ..orders.models import Order
from .models import serializers


class ShopViewset(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.ShopItemSerializer
    queryset = models.Item.objects.all()

    @swagger_auto_schema(
        method="POST",
        security=[],
        operation_summary="Create Payment",
        request_body=no_body,
        responses={
            status.HTTP_201_CREATED: serializers.CreateOrderResponseSerializer(),
        }
    )
    @action(detail=True, methods=["post"], name="Create Payment")
    def payment(self, request: Request, pk: str) -> Response:
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
        order_id = order.pk.hex
        res = paypal.create_payment(
            price=price, reference=order_id, currency=currency
        )
        paypal_order_id = res.result.id
        order.related_paypal_order = paypal_order_id
        order.save()
        return Response({
            "system_order_id": order_id,
            "paypal_order_id": paypal_order_id
        }, 201)
