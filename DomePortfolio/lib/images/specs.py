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


class ThumbnailSpec(Spec):
    processors = [
        ResizeToFit(640, 360)
    ]
    format = "PNG"
    options = {"quality": 90, "optimize": True}


__all__ = ["ImageSpec", "ThumbnailSpec"]
