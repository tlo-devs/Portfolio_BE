from adminsortable2.admin import SortableInlineAdminMixin
from django import forms
from django.contrib import admin
from django.forms import ImageField
from django.http import HttpResponseRedirect

from .models import Item, Image, Order
from ...lib.widgets import ImagePreviewWidget
from django.contrib import messages
from django.utils.translation import ngettext, gettext_lazy
from django.shortcuts import render
from django.contrib.admin import SimpleListFilter


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


class OrderFilter(SimpleListFilter):
    title = gettext_lazy("Filter")

    parameter_name = "completed"

    def lookups(self, request, model_admin):
        return (
            (None, "Completed"),
            ("pending", "Pending"),
            ("all", "All")
        )

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == 'pending':
            return queryset.filter(
                completed=True if self.value() is "completed" else False
            )
        elif self.value() is None:
            return queryset.filter(completed=True)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = [OrderFilter]
    list_display = ("product", "completed", "pk")

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
