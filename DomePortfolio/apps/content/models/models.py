from django.db import models
from imagekit.models import ProcessedImageField
from DomePortfolio.lib.storage.gcp_storage import ImageStorage
from DomePortfolio.lib.images.specs import ShopImageSpec


class AboutSection(models.Model):
    img = ProcessedImageField(
        spec=ShopImageSpec,
        storage=ImageStorage(),
        null=True
    )

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self) -> str:
        return "About Section"


class ParagraphBase(models.Model):
    order_field = models.PositiveSmallIntegerField(
        default=0,
        null=False,
        blank=False,
        unique=False
    )
    text = models.CharField(max_length=255)

    class Meta:
        abstract = True
        ordering = ["order_field"]


class AboutParagraph(ParagraphBase):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey(
        to=AboutSection,
        on_delete=models.CASCADE,
        related_name="about"
    )

    def __str__(self) -> str:
        return f"About Paragraph Nr. {self.order_field} of {str(self.parent)}"


class VitaParagraph(ParagraphBase):
    year = models.PositiveSmallIntegerField()
    parent = models.ForeignKey(
        to=AboutSection,
        on_delete=models.CASCADE,
        related_name="vita"
    )

    def __str__(self) -> str:
        return f"Vita Paragraph Nr. {self.order_field} of {str(self.parent)}"


__all__ = ["AboutSection", "AboutParagraph", "VitaParagraph"]
