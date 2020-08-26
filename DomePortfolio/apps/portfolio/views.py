from rest_framework import mixins, viewsets

from .models import models
from .models import serializers


class PortfolioImageViewset(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = serializers.ImageItemSerializer
    queryset = models.ImageItem.objects.all()


class PortfolioVideoViewset(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = serializers.VideoItemSerializer
    queryset = models.VideoItem.objects.all()
