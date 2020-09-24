from rest_framework import serializers
from . import models


class AboutParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AboutParagraph
        fields = ("title", "text")


class VitaParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VitaParagraph
        fields = ("year", "text")


class AboutSectionSerializer(serializers.Serializer):  # noqa must implement abstract
    about = AboutParagraphSerializer(
        many=True,
        read_only=True
    )
    vita = VitaParagraphSerializer(
        many=True,
        read_only=True
    )

    def to_representation(self, instance):
        data = super(AboutSectionSerializer, self).to_representation(instance)
        data["img"] = instance.img.name or None
        return data


class HomeSectionSerializer(serializers.Serializer):  # noqa must implement abstract
    video_desktop = serializers.FileField()
    video_mobile = serializers.FileField()

    def to_representation(self, instance):
        data = super(HomeSectionSerializer, self).to_representation(instance)
        data["video_desktop"] = instance.video_desktop.name or None
        data["video_mobile"] = instance.video_mobile.name or None
        return data
