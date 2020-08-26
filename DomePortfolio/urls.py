from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from .apps.users.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .docs.openapi import schema_view

urlpatterns = [
    # Included URL paths
    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    url(r'^api-auth/', include('rest_framework.urls')),

    # Authentication URL paths
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User defined URL paths
    path("categories/", include("DomePortfolio.apps.categories.urls")),
    path("portfolio/", include("DomePortfolio.apps.portfolio.urls")),
    path("shop/", include("DomePortfolio.apps.shop.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
