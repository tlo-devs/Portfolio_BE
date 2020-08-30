from rest_framework import routers

from . import views

app_name = "shop"

router = routers.SimpleRouter()
router.register(r"", views.ShopViewset)

urlpatterns = []

urlpatterns += router.urls
