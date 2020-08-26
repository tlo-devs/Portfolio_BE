from random import choice
from string import ascii_lowercase

from django.forms import FileInput, TextInput
from django.utils.safestring import mark_safe


class ImagePreviewWidget(FileInput):
    template_name = "extrawidgets/image_preview.html"
    base_id = "admin-image-preview-widget"

    def render(self, name, value, attrs=None, renderer=None):
        random_lowercase_letters = [choice(ascii_lowercase) for _ in range(10)]
        attrs["id"] = f"{self.base_id}-{''.join(random_lowercase_letters)}"
        widget = super(ImagePreviewWidget, self).render(name, value, attrs, renderer)
        return mark_safe(widget)

    def format_value(self, value):
        """Override default widget behaviour so a preview can be displayed"""
        return value


class VideoPreviewWidget(TextInput):
    template_name = "extrawidgets/video_preview.html"
    base_id = "admin-video-preview-widget"

    def render(self, name, value, attrs=None, renderer=None):
        random_lowercase_letters = [choice(ascii_lowercase) for _ in range(10)]
        attrs["id"] = f"{self.base_id}-{''.join(random_lowercase_letters)}"
        widget = super(VideoPreviewWidget, self).render(name, value, attrs, renderer)
        return mark_safe(widget)


__all__ = ["ImagePreviewWidget", "VideoPreviewWidget"]
