from django.conf import settings
from paypalhttp.http_response import HttpResponse


class MockPayPalOrder:
    def __init__(self, *,
                 paypal_id: str,
                 price: str,
                 currency: str,
                 reference: str) -> None:
        self.price = price
        self.currency = currency
        self.reference = reference
        self.id = paypal_id
        self.status = "CREATED"
        self.intent = None

    def approve(self):
        self.status = "APPROVED"

    def complete(self):
        self.status = "COMPLETED"
        self.intent = "CAPTURE"


class PayPalTestClient:
    """
    This class takes an existing PayPal order
    and mocks the rest of its lifecycle based on the initial data.
    """

    def __init__(self, paypal_order_id: str):
        client = PayPalClient(
            client_id=settings.PAYPAL_CLIENT,
            client_secret=settings.PAYPAL_SECRET,
            sandbox=True
        )
        order = client.get_payment(paypal_order_id)
        data = order.result
        self._order = MockPayPalOrder(
            paypal_id=data.id,
            reference=data.purchase_units.reference_id,
            price=data.purchase_units.amount.value,
            currency=data.purchase_units.amount.currency_code
        )

    def complete_payment(self):
        self._order.complete()
        response_data = {
            "id": self._order.id,
            "intent": self._order.intent,
            "status": self._order.status,
            "purchase_units": [
                {
                    "reference_id": self._order.reference,
                    "amount": {
                        "currency_code": self._order.currency,
                        "value": self._order.price,
                    },
                    "payee": {
                        "email_address": "sb-utijy1297964@personal.example.com",
                        "merchant_id": "Q7HS8BJ65TDC6"
                    },
                }
            ],
            "payer": {
                "name": {
                    "given_name": "John",
                    "surname": "Doe"
                },
                "email_address": "sb-7uolw1287648@personal.example.com",
                "payer_id": "DMNWL4LPAT23G",
                "address": {
                    "country_code": "DE"
                }
            },
        }
        response = HttpResponse(
            response_data,
            status_code=200
        )
        return response


__all__ = ["PayPalTestClient", "MockPayPalOrder"]
