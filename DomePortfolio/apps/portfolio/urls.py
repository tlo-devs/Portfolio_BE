from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"image", views.PortfolioImageViewset)
router.register(r"video", views.PortfolioVideoViewset)

urlpatterns = []

urlpatterns += router.urls
