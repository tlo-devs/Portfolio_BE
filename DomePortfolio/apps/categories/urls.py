from django.urls import path
from rest_framework import routers
from . import views

app_name = "categories"

router = routers.SimpleRouter()

urlpatterns = [
    path("<str:root_key>/", views.category),
]

urlpatterns += router.urls
