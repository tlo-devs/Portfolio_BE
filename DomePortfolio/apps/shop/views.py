import datetime
from decimal import Decimal, ROUND_HALF_EVEN

import requests
from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.utils.cache import patch_cache_control
from itsdangerous import TimestampSigner
from itsdangerous.exc import SignatureExpired, BadSignature, BadTimeSignature
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response

from DomePortfolio.lib.payments.paypal import PayPalClient
from .models import models
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
        order = models.Order.objects.create(
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
            "paypal_order_id": res.result.id,
            "internal_order_id": str(order.pk),
        }, 201)


@api_view(["GET"])
def complete_order(request, paypal_order_id: str):
    paypal = PayPalClient(
        sandbox=settings.PAYPAL_SANDBOX,
        client_id=settings.PAYPAL_CLIENT,
        client_secret=settings.PAYPAL_SECRET,
    )
    res = paypal.get_payment(paypal_order_id)
    if res.result.status != "COMPLETED":
        return Response({
            "error": "INVALID_ORDER_STATUS",
            "msg": "PayPal Order Status must be 'COMPLETED'"
        }, 400)

    purchase = res.result.purchase_units
    payer = res.result.payer

    order = models.Order.objects.get(pk=purchase.reference_id)
    current_time = datetime.datetime.now()
    download_time = current_time + datetime.timedelta(
        seconds=settings.DOWNLOAD_EXPIRY_TIME
    )

    params = {
        "completed": True,
        "ordered_on": current_time,
        "customer_email": payer.email_address,
        "customer_id": payer.payer_id,
        "product_downloads_remaining": 1,
        "download_expires_on": download_time,
    }
    for key, item in params.items():
        setattr(order, key, item)
    order.save()

    signer = TimestampSigner(settings.SECRET_KEY)
    download_url = signer.sign(order.pk)
    return Response({
        "paypal_order_id": "",
        "internal_order_id": "",
        "internal_product_id": 1,
        "status": "VALID_ORDER",
        "grant_url": download_url
    })


@api_view(["GET"])
def download_with_order(request, grant: str):
    signer = TimestampSigner(settings.SECRET_KEY)
    try:
        order_pk = signer.unsign(grant, max_age=settings.DOWNLOAD_EXPIRY_TIME)
    except SignatureExpired or BadSignature or BadTimeSignature:
        return Response({
            "error": "BAD_SIGNATURE",
            "msg": "Invalid Signature"
        }, 400)
    order = get_object_or_404(models.Order.objects.all(), pk=order_pk)
    download_url = order.product.download.url
    download_name = order.product.download.name
    req = requests.get(
        download_url, stream=True
    )
    res = StreamingHttpResponse(streaming_content=req)
    res["Content-Disposition"] = f"attachement; filename='{download_name}'"
    res["Cache-Control"] = "no-store"
    patch_cache_control(res, max_age=0, public=True)
    return res
