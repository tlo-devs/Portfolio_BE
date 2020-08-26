from django.urls import re_path
from rest_framework import routers
from . import views


router = routers.SimpleRouter()

urlpatterns = [
    re_path(r"shop/|portfolio/", views.category),
]

urlpatterns += router.urls
