from typing import Optional

from PIL import Image
from PIL.PngImagePlugin import PngImageFile


class ResizeToFitAspectRatio:
    def __init__(
            self,
            /,
            aspect: Optional[tuple] = None,
            *,
            vertical_aspect: Optional[int] = None,
            horizontal_aspect: Optional[int] = None,
    ) -> None:
        if (aspect is None) and (vertical_aspect is None and horizontal_aspect is None):
            raise ValueError("Either an aspect tuple,"
                             "or seperate aspect integers have to be provided.")
        self.va, self.ha = aspect or (vertical_aspect, horizontal_aspect)
        self.aspect = self.ha / self.va

    def process(self, image: PngImageFile) -> Image.Image:
        width, height = image.width, image.height
        current_aspect = width / height

        # Crop the image to a 16:9 aspect ratio
        if current_aspect > self.aspect:
            # Crop the left and right edges
            new_width = int(self.aspect * height)
            offset = (width - new_width) / 2
            resize = (offset, 0, width - offset, height)
        else:
            # Crop the top and bottom
            new_height = int(width / self.aspect)
            offset = (height - new_height) / 2
            resize = (0, offset, width, height - offset)
        return image.crop(resize)


__all__ = ["ResizeToFitAspectRatio"]
