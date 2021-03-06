from adminsortable2.admin import SortableInlineAdminMixin
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.db import OperationalError, ProgrammingError
from django.forms import ImageField, IntegerField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ngettext, gettext_lazy
from mptt.forms import TreeNodeChoiceField

from DomePortfolio.apps.categories.models import CategoryTree
from .models import Item, Image, Download
from ...lib.widgets import ImagePreviewWidget


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0
    classes = ["collapse"]
    max_num = 10
    min_num = 1


class ShopItemForm(forms.ModelForm):
    thumbnail = ImageField(widget=ImagePreviewWidget)
    sale = IntegerField(
        min_value=0,
        max_value=100,
        help_text="Item price reduction (sale) in percent",
    )
    download = forms.FileField()
    try:
        category = TreeNodeChoiceField(
            queryset=CategoryTree.shop.get_parent_leaves("digital"),
            level_indicator=""
        )
    except OperationalError or ProgrammingError:
        pass

    def _post_clean(self):
        if "download" in self.changed_data:
            dl = Download.objects.create(
                file=self.cleaned_data.get("download")
            )
            dl.save()
        else:
            dl = self.instance.download
        self.cleaned_data["download"] = dl
        super(ShopItemForm, self)._post_clean()

    class Meta:
        model = Item
        fields = "__all__"


@admin.register(Item)
class ShopItemAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    actions = ["initiate_sale"]
    form = ShopItemForm

    def initiate_sale(self, request, queryset):
        if "apply" in request.POST:
            updated = queryset.update(
                sale=int(request.POST.get("sale_amount"))
            )
            self.message_user(request, ngettext(
                '%d product was successfully updated.',
                '%d products were successfully updated.',
                updated,
            ) % updated, messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())
        return render(
            request,
            "shop/sale_action.html",
            {"items": queryset}
        )

    initiate_sale.short_description = gettext_lazy("Start Sale")
