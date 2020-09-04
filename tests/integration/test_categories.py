from django.test import TestCase, Client


class CategoryTestCase(TestCase):
    def setUp(self) -> None:
        self.testing_client = Client()

    def test_category_view(self):
        # We are not reversing the URL here as reverse does not
        # support Regex URLs with an OR operator
        base_url = "/categories/%s/"
        options = ("shop", "portfolio")
        for url in options:
            res = self.testing_client.get(
                base_url % url
            )
            assert res.status_code == 200
        options = ("wrong", "shops", "sth")
        for url in options:
            res = self.testing_client.get(
                base_url % url
            )
            assert res.status_code == 404
