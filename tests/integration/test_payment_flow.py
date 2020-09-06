from decimal import Decimal
from pathlib import Path
from unittest import mock

from django.http import QueryDict
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from DomePortfolio.apps.shop.models import Item as ShopItem
from DomePortfolio.lib.payments.paypal import MockPayPalResponse
from DomePortfolio.lib.storage.gcp_storage import FileStorage


class PaymentFlowTestCase(TestCase):
    def setUp(self) -> None:
        self.testing_client = Client()
        with open(Path(
            "/c/Users/kochb/Downloads/serverless-image-handler.template"
        ), "r") as fin:
            self.item = ShopItem.objects.create(
                title="Test Item",
                thumbnail="",
                price=Decimal("10.0000"),
                price_currency="EUR",
                download=FileStorage().save(
                    fin.name, content=fin
                )
            )

    def test_payment_flow(self):
        """
        Tests the applications payment flow,
        the following flow is expected:
        1. (Create a shop_item)
        2. Generate a PayPal order from a shop_item | CREATE
        3. (An order gets approved on the Frontend) | AUTHORIZE, CAPTURE, PATCH
        4. Mark the order as completed on the backend,
        we also return a download grant in this step
        5. The user can download their product for a limited time

        This test assumes the existence of already created shop_items
        """
        # Call create_payment
        res = self.testing_client.get(
            reverse("shop:item-payment", args=(self.item.pk,))
        )
        assert res.status_code == status.HTTP_201_CREATED
        order_id = res.json().get("order")

        # Mock the associated PayPal order lifecycle
        patch = mock.patch(
            "DomePortfolio.apps.orders.views.PayPalClient",
            is_payment_completed=True,
        )
        with patch as patched_client:
            patched_client.return_value.get_payment.return_value = MockPayPalResponse(
                    purchase_units={"reference_id": order_id},
                    payer={
                        "payer_id": "dfghjklkjhgfg",
                        "email_address": "m@uri.ce"
                    }
                )
            # Complete the order on backend
            res = self.testing_client.get(
                reverse("orders:complete", args=(order_id,))
            )
        assert res.status_code == status.HTTP_201_CREATED
        data = res.json()
        order_id, grant = data.get("order_id"), data.get("grant")

        # Test the download functionality via grant
        q_args = QueryDict("", mutable=True)
        q_args["grant"] = grant
        res = self.testing_client.get(
            "{base_url}?{query_args}".format(
                base_url=reverse('orders:download', args=(order_id,)),
                query_args=q_args.urlencode()
            )
        )
        assert res.status_code == status.HTTP_200_OK
