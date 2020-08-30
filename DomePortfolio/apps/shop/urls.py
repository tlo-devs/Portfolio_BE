from rest_framework import routers
from django.urls import path

from . import views

app_name = "shop"

router = routers.SimpleRouter()
router.register(r"", views.ShopViewset)

urlpatterns = [
    path("orders/<str:paypal_order_id>/capture", views.complete_order, name="capture"),
    path("orders/<str:grant>/download", views.download_with_order, name="download")
]

urlpatterns += router.urls
