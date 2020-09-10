from imagekit.processors import ResizeToFit
from imagekit.specs import ImageSpec as Spec
from .processors import ResizeToFitAspectRatio


class ImageSpec(Spec):
    processors = [
        ResizeToFitAspectRatio(
            horizontal_aspect=16, vertical_aspect=9,
        ),
        ResizeToFit(width=1920, height=1080),
    ]
    format = "PNG"
    options = {"quality": 90, "optimize": True}


class ShopImageSpec(Spec):
    processors = [
        ResizeToFitAspectRatio(
            horizontal_aspect=4, vertical_aspect=5,
        ),
        ResizeToFit(width=1120, height=1400),
    ]
    format = "PNG"
    options = {"quality": 90, "optimize": True}


class ThumbnailSpec(Spec):
    processors = [
        ResizeToFitAspectRatio(
            horizontal_aspect=16, vertical_aspect=9,
        ),
        ResizeToFit(640, 360)
    ]
    format = "PNG"
    options = {"quality": 90, "optimize": True}


__all__ = ["ImageSpec", "ShopImageSpec", "ThumbnailSpec"]
