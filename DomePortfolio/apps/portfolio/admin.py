from typing import Type

from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.db.utils import OperationalError
from django.forms import ModelForm, ImageField
from mptt.forms import TreeNodeChoiceField

from .models import ImageItem, VideoItem, Image
from ..categories.models import CategoryTree
from ...lib.widgets import ImagePreviewWidget, VideoPreviewWidget
import contextlib


def form_factory(toplevel_category: str) -> Type[ModelForm]:
    m = ImageItem if toplevel_category == "image" else VideoItem

    with contextlib.suppress(OperationalError):
        class PortfolioModelForm(ModelForm):
            category = TreeNodeChoiceField(
                queryset=CategoryTree.portfolio.get_parent_leaves(toplevel_category),
                level_indicator=""
            )
            thumbnail = ImageField(widget=ImagePreviewWidget)

            class Meta:
                model = m
                fields = "__all__"
                widgets = {
                    'video': VideoPreviewWidget
                }
    return PortfolioModelForm


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0
    classes = ["collapse"]
    formfield_overrides = {
        models.ImageField: {'widget': ImagePreviewWidget}
    }
    max_num = 50
    min_num = 1


@admin.register(ImageItem)
class PortfolioImageAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    fieldsets = (
        (None, {
            "fields": (
                ("title", "category"),
                "thumbnail",
                ("client", "year"),
                "description"
            )
        }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        return form_factory("image")


@admin.register(VideoItem)
class PortfolioVideoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                ("title", "category"),
                "thumbnail",
                ("client", "year"),
                "description",
                "video"
            )
        }),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        return form_factory("video")

    def save_model(self, request: WSGIRequest, obj, form, change) -> None:
        setattr(obj, "video", request.POST.get("video-id"))
        super(PortfolioVideoAdmin, self).save_model(request, obj, form, change)
