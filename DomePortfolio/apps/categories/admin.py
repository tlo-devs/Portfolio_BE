from typing import Optional, Type

from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField
from django.forms import ModelForm, HiddenInput, CharField

from .models import CategoryTree


class CategoryTreeAddForm(ModelForm):
    parent = TreeNodeChoiceField(
        queryset=CategoryTree.objects.all().filter(
            children__isnull=False, parent__isnull=False
        ).distinct(),
        level_indicator=""
    )
    key = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = CategoryTree
        fields = ["name", "key", "parent"]


class CategoryTreeEditForm(ModelForm):
    class Meta:
        model = CategoryTree
        fields = ["name"]


@admin.register(CategoryTree)
class CategoryTreeAdmin(MPTTModelAdmin):
    list_display = ('category_name',)
    list_display_links = ('category_name',)
    mptt_level_indent = 50

    form = CategoryTreeAddForm

    def category_name(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            self.mptt_level_indent,
            instance.name,
        )
    category_name.short_description = "Kategoriename"

    # noinspection PyMethodMayBeStatic
    def is_leaf(self, obj: Optional[CategoryTree]):
        if obj is not None and obj.key != "all":
            return obj.is_leaf_node()
        return False

    def has_change_permission(self,
                              request,
                              obj: Optional[CategoryTree] = None
                              ) -> bool:
        return self.is_leaf(obj)

    def has_delete_permission(self,
                              request,
                              obj: Optional[CategoryTree] = None
                              ) -> bool:
        return self.is_leaf(obj)

    def get_form(
            self,
            request,
            obj=None,
            change=False,
            **kwargs
    ) -> Type[ModelForm]:
        if not obj:
            return CategoryTreeAddForm
        return CategoryTreeEditForm
    
    def save_model(self, request, obj, form, change):
        obj.key = obj.name.lower()
        super(CategoryTreeAdmin, self).save_model(
            request, obj, form, change
        )
