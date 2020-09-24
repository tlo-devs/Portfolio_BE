from django.urls import path
from rest_framework import routers
from . import views

app_name = "content"

router = routers.SimpleRouter()

urlpatterns = [
    path("about/", views.about_view),
    path("home/", views.home_view)
]

urlpatterns += router.urls
