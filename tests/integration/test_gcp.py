import pytest
from django.conf import settings
from DomePortfolio.lib.storage.gcp_storage import GCPStorage


def test_exists():
    """
    Tests for the existence of the GCP storage buckets,
    that are specified in the settings
    """
    pass


def test_acl():
    """
    Checks to make sure the ACLs are correctly set for all buckets
    """
    pass
