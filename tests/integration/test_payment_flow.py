from DomePortfolio.lib.payments.paypal import PayPalTestClient
from django.test import TestCase, Client
from DomePortfolio.apps.shop.models import Item
from decimal import Decimal
from django.urls import reverse


BASE_URL = "http://localhost:8000/shop"


class PaymentFlowTestCase(TestCase):
    def setUp(self) -> None:
        self.testing_client = Client()
        Item.objects.create(
            title="Test Item",
            thumbnail="",
            price=Decimal("10.0000"),
            price_currency="EUR",
            download=""
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
        client = self.testing_client

        # Call create_payment
        res = client.get(f"{BASE_URL}/1/payment/")
        assert res.status_code == 201
        data = res.json()
        paypal_order_id = data.get("paypal_order_id")

        # Mock the remaining lifecycle of the order
        order = PayPalTestClient(paypal_order_id)
        order.complete_payment()

        # Complete the order on the Backend
        res = client.get(
            reverse("shop:capture", args=(paypal_order_id,))
        )
        assert res.status_code == 200
        data = res.data.json()
        grant = data.get("grant_url")

        # Test the download functionality via grant
        res = client.get(f"{BASE_URL}/{grant}/download/")
        assert res.status_code == 200
