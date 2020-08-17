from django.urls import path
from rest_framework import routers
from . import views


router = routers.SimpleRouter()

urlpatterns = [
    path("shop/", views.shop),
    path("portfolio/", views.portfolio),
]

urlpatterns += router.urls
