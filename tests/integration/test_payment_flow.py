from DomePortfolio.lib.payments.paypal import PayPalTestClient


BASE_URL = "http://localhost:8000/shop"


def test_payment_flow(get_testing_client):
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
    client = get_testing_client()

    # Call create_payment
    res = client.get(f"{BASE_URL}/1/payment/")
    assert res.status_code == 200
    data = res.data.json()
    paypal_order_id = data.get("paypal_order_id")

    # Mock the remaining lifecycle of the order
    order = PayPalTestClient(paypal_order_id)

    # Complete the order on the Backend
    res = client.get(f"{BASE_URL}/orders/{paypal_order_id}/capture/")
    assert res.status_code == 200
    data = res.data.json()
