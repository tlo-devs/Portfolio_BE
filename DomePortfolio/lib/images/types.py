from typing import Type

from django.db import models
from rest_framework import serializers


class BaseImage(models.Model):
    image: models.ImageField
    parent_item: models.ForeignKey

    order_field = models.PositiveSmallIntegerField(
        default=0,
        null=False,
        blank=False,
        unique=False
    )

    class Meta:
        abstract = True
        ordering = ["order_field"]

    def __str__(self) -> str:
        return self.image.name

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        """
        Connect all of our concrete subclasses,
        to the post delete event of our abstract base class.
        """
        super().__init_subclass__(**kwargs)
        models.signals.post_delete.connect(  # connect the callback function
            delete_remote_instances, sender=cls
        )


class BaseImageSerializer(serializers.Serializer):  # noqa must implement abstract
    image = serializers.URLField()
    order_field = serializers.IntegerField(write_only=True)

    def to_representation(self, instance) -> dict:
        return {"image": instance.image.name}


def delete_remote_instances(
        sender: Type[BaseImage],
        instance: BaseImage,
        using: str,
        **kwargs
        ) -> None:
    uri = instance.image.name
    if "/" in uri:
        uri = uri.split("/")[-1]
    storage = instance.image.storage
    storage.delete(uri)


__all__ = ["BaseImage", "BaseImageSerializer"]
