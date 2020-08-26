from typing import ClassVar

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersGetRequest
from paypalhttp.http_response import HttpResponse


class PayPalClient:
    __interned: ClassVar[dict] = {}

    def __new__(cls, *,
                sandbox: bool,
                client_id: str,
                client_secret: str,
                **kwargs) -> "PayPalClient":
        key = (sandbox, client_id, client_secret)
        if not cls.__interned.get(key):
            _creds = {
                "client_id": client_id,
                "client_secret": client_secret
            }
            env = (SandboxEnvironment if sandbox else LiveEnvironment)(**_creds)

            obj = super().__new__(cls)
            obj.environment = env
            obj.id = client_id
            obj.secret = client_secret
            obj.client = PayPalHttpClient(env)
            cls.__interned[key] = obj
        return cls.__interned[key]

    def create_payment(self, *,
                       price: str,
                       currency: str,
                       reference: str) -> HttpResponse:
        """
        Create a new PayPal payment that gets authorized on the Frontend

        :param currency: Currencies international abbreviation, e.g. EUR, USD
        :param reference: A given reference ID for the PayPal order
        :param price: Price of the product with 2 digits precision
        :return: The response of the API call to PayPal
        """
        request = OrdersCreateRequest()
        request.prefer("return=representation")
        request.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": reference,
                "amount": {
                    "currency_code": currency,
                    "value": price,
                }
            }]
        })
        return self.client.execute(request)

    def get_payment(self, order_id: str) -> HttpResponse:
        """
        Retrieve details for a PayPal payment

        :param order_id: ID of the PayPal payment
        :return: The response of the API call to PayPal
        """
        request = OrdersGetRequest(order_id)
        return self.client.execute(request)
