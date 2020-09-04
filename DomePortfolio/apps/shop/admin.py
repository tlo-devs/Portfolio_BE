from adminsortable2.admin import SortableInlineAdminMixin
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.forms import ImageField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ngettext, gettext_lazy

from .models import Item, Image
from ...lib.widgets import ImagePreviewWidget


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0
    classes = ["collapse"]
    max_num = 50
    min_num = 1


class ShopItemCreateForm(forms.ModelForm):
    thumbnail = ImageField(widget=ImagePreviewWidget)

    class Meta:
        model = Item
        fields = "__all__"
        exclude = ("sale",)


class ShopItemChangeForm(forms.ModelForm):
    thumbnail = ImageField(widget=ImagePreviewWidget)

    class Meta:
        model = Item
        fields = "__all__"


@admin.register(Item)
class ShopItemAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    actions = ["initiate_sale"]

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not change:
            return ShopItemCreateForm
        return ShopItemChangeForm

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
