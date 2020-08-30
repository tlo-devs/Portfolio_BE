from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from .apps.users.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .docs.openapi import schema_view

urlpatterns = [
    # Included URL paths
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    re_path(r'^api-auth/', include('rest_framework.urls')),

    # Authentication URL paths
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User defined URL paths
    path("categories/", include("DomePortfolio.apps.categories.urls", namespace="categories")),
    path("portfolio/", include("DomePortfolio.apps.portfolio.urls", namespace="portfolio")),
    path("shop/", include("DomePortfolio.apps.shop.urls", namespace="shop")),
    path("orders/<str:order_id>/", include("DomePortfolio.apps.orders.urls", namespace="orders"))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
