import datetime

from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.utils.cache import patch_cache_control
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
from itsdangerous import TimestampSigner
from itsdangerous.exc import BadSignature, SignatureExpired, BadTimeSignature
from rest_framework.decorators import api_view
from rest_framework.response import Response

from DomePortfolio.lib.payments.paypal import PayPalClient
from DomePortfolio.lib.utils import uuid4_is_valid
from .models import Order


@api_view(["GET"])
def complete_order(request, order_id: str):
    if not uuid4_is_valid(order_id):
        return Response(status=404)
    order = get_object_or_404(Order.objects.all(), pk=order_id)

    paypal_order_id = order.related_paypal_order
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

    order = Order.objects.get(pk=purchase.reference_id)
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
        "paypal_order_id": purchase.reference_id,
        "internal_order_id": str(order.pk),
        "internal_product_id": order.product.id,
        "status": "VALID_ORDER",
        "grant_url": download_url
    })


@api_view(["GET"])
def download_with_order(request, order_id: str):
    if not uuid4_is_valid(order_id):
        return Response(status=404)
    grant = request.query_params.get("grant", None)
    if grant is None:
        return Response({
            "info": "'grant' is required as a query argument"
        }, 400)

    order = get_object_or_404(Order.objects.all(), pk=order_id)
    signer = TimestampSigner(settings.SECRET_KEY)
    try:
        order_pk = signer.unsign(grant, max_age=settings.DOWNLOAD_EXPIRY_TIME)
    except SignatureExpired or BadSignature or BadTimeSignature:
        return Response({
            "error": "BAD_SIGNATURE",
            "msg": "Invalid Signature"
        }, 400)
    if not order_pk == order_id:
        return Response(status=400)

    download_url = order.product.download.url
    download_name = order.product.download.name

    credentials = service_account.Credentials.from_service_account_file(
        settings.GCP_KEYFILE_PATH / "CLOUD_STORAGE_OPERATOR.json"
    )
    sess = AuthorizedSession(credentials)
    req = sess.get(
        download_url, stream=True
    )
    res = StreamingHttpResponse(streaming_content=req)

    res["Content-Disposition"] = f"attachement; filename='{download_name}'"
    res["Cache-Control"] = "no-store"
    patch_cache_control(res, max_age=0, public=True)
    return res
