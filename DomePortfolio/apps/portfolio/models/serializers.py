from rest_framework import serializers
from .models import ImageItem, VideoItem, Image
from ....lib.images.types import BaseImageSerializer


class ImageItemSerializer(serializers.ModelSerializer):
    images = BaseImageSerializer(
        many=True,
        read_only=True
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="key"
    )
    id = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = ImageItem
        fields = "__all__"

    def to_representation(self, instance):
        data = super(ImageItemSerializer, self).to_representation(instance)
        data["thumbnail"] = instance.thumbnail.name
        return data


class VideoItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="key"
    )

    class Meta:
        model = VideoItem
        fields = "__all__"

    def to_representation(self, instance):
        data = super(VideoItemSerializer, self).to_representation(instance)
        data["thumbnail"] = instance.thumbnail.name
        return data
