from django.urls import path
from rest_framework import routers
from . import views

app_name = "orders"

router = routers.SimpleRouter()

urlpatterns = [
    path("complete/", views.complete_order, name="complete"),
    path("download/", views.download_with_order, name="download")
]

urlpatterns += router.urls
