from adminsortable2.admin import SortableInlineAdminMixin
from django import forms
from django.contrib import admin

from DomePortfolio.lib.widgets import ImagePreviewWidget
from .models.models import AboutParagraph, AboutSection, VitaParagraph, HomeSection


class AboutParagraphChangeForm(forms.ModelForm):
    img = forms.ImageField(widget=ImagePreviewWidget, required=False)

    class Meta:
        model = AboutSection
        fields = "__all__"


class AboutParagrahsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = AboutParagraph
    extra = 0
    classes = ["collapse"]
    max_num = 50
    min_num = 1
    fields = ("title", "text")


class VitaParagraphsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = VitaParagraph
    extra = 0
    classes = ["collapse"]
    max_num = 50
    min_num = 1
    fields = ("year", "text")


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    inlines = [AboutParagrahsInline, VitaParagraphsInline]
    form = AboutParagraphChangeForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True
