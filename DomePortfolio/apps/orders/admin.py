from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy
from .models import Order


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
                completed=True if self.value() == "completed" else False
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
