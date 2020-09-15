import datetime
from typing import Union

from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.utils.cache import patch_cache_control
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
from itsdangerous import TimestampSigner
from itsdangerous.exc import BadSignature, SignatureExpired, BadTimeSignature
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from DomePortfolio.lib.payments.paypal import PayPalClient
from DomePortfolio.lib.utils import uuid4_is_valid
from .models import Order
from .models import serializers as app_serializers


@swagger_auto_schema(
    method="POST",
    operation_summary="Complete Order",
    operation_description="Complete an order on the Backend, "
                          "after the PayPal payment has been completed",
    security=[],
    responses={
        status.HTTP_201_CREATED: app_serializers.CompleteOrderSerializer(),
        status.HTTP_400_BAD_REQUEST: app_serializers.ErrorSerializer(),
    }
)
@api_view(["POST"])
def complete_order(request: Request,
                   order_id: str) -> Response:
    # Validate that the order exists and is a valid UUIDv4
    if not uuid4_is_valid(order_id):
        return Response(status=404)
    order = get_object_or_404(Order.objects.all(), pk=order_id)

    # Validate the status of the corresponding PayPal order
    paypal_order_id = order.related_paypal_order
    paypal = PayPalClient(
        sandbox=settings.PAYPAL_SANDBOX,
        client_id=settings.PAYPAL_CLIENT,
        client_secret=settings.PAYPAL_SECRET,
    )
    res = paypal.get_payment(paypal_order_id)
    if not paypal.is_payment_completed(paypal_order_id):
        return Response({
            "error": "INVALID_ORDER_STATUS",
            "msg": "PayPal Order Status must be 'COMPLETED'"
        }, 400)

    # Update the order with the captured data
    reference_id = res.result.purchase_units.reference_id
    payer = res.result.payer
    payer_id = payer.payer_id
    payer_email = payer.email_address
    current_time = timezone.now()
    download_time = current_time + datetime.timedelta(
        seconds=settings.DOWNLOAD_EXPIRY_TIME
    )
    params = {
        "completed": True,
        "product_downloads_remaining": 1,
        "ordered_on": current_time,
        "customer_email": payer_email,
        "customer_id": payer_id,
        "download_expires_on": download_time,
    }
    for key, item in params.items():
        setattr(order, key, item)
    order.save()

    # Encode the grant and send it to the client
    signer = TimestampSigner(settings.SECRET_KEY)
    download_url = signer.sign(order.pk.hex)
    return Response({
        "order_id": reference_id,
        "grant": download_url
    }, 201)


@swagger_auto_schema(
    method="GET",
    operation_summary="Download Item",
    operation_description="Download the purchased digital good "
                          "via a grant received after purchase",
    security=[],
    responses={
        status.HTTP_200_OK: "Returns the downloadable content",
        status.HTTP_400_BAD_REQUEST: app_serializers.ErrorSerializer(),
        status.HTTP_404_NOT_FOUND: "",
    },
    query_serializer=app_serializers.QueryArgsSerializer(),
)
@api_view(["GET"])
def download_with_order(request: Request,
                        order_id: str
                        ) -> Union[Response, StreamingHttpResponse]:
    # Validate that the order exists and is a valid UUIDv4
    # We also check if the grant query argument exists
    if not uuid4_is_valid(order_id):
        return Response(status=404)
    grant = request.query_params.get("grant", None)
    if grant is None:
        return Response({
            "error": "MISSING_ARGS",
            "msg": "'grant' is required as a query argument"
        }, 400)
    order = get_object_or_404(Order.objects.all(), pk=order_id)

    # Validate that the grant is valid
    signer = TimestampSigner(settings.SECRET_KEY)
    try:
        order_pk = signer.unsign(grant, max_age=settings.DOWNLOAD_EXPIRY_TIME)
        order_pk = order_pk.decode()
    except SignatureExpired or BadSignature or BadTimeSignature:
        return Response({
            "error": "BAD_SIGNATURE",
            "msg": "Invalid Signature"
        }, 400)
    if not order_pk == order_id:
        return Response(status=404)

    download_url = order.product.download.name
    download_name = "file"

    # Authenticate to Cloud Storage and prepare a streaming request,
    # for the users file download
    credentials = service_account.Credentials.from_service_account_file(
        settings.GCP_KEYFILE_PATH / "CLOUD_STORAGE_OPERATOR.json",
        scopes=["https://www.googleapis.com/auth/devstorage.read_only"]
    )
    sess = AuthorizedSession(credentials)
    req = sess.get(
        download_url, stream=True
    )
    res = StreamingHttpResponse(streaming_content=req)

    # Adjust the headers for the download and send the response
    res["Content-Disposition"] = f"attachement; filename='{download_name}'"
    res["Cache-Control"] = "no-store"
    patch_cache_control(res, max_age=0, public=True)
    return res
