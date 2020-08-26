from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class RootManager(models.Manager):
    root_key: str

    def get_queryset(self):
        root_id = super(RootManager, self).get_queryset().get(
            key=self.root_key
        ).id
        return super(RootManager, self).get_queryset().filter(tree_id=root_id)

    def get_parent_leaves(self, parent_key: str):
        all_ = super(RootManager, self).get_queryset()
        leaves = [
            l for l in all_.filter(
                children__isnull=True
            ) if l.get_root().key == self.root_key
                 and l.key != "all"
                 and l.parent.key == parent_key
        ]
        return self.filter(id__in=[node.id for node in leaves])


class PortfolioManager(RootManager):
    root_key = "portfolio"


class ShopManager(RootManager):
    root_key = "shop"


class CategoryTree(MPTTModel):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children'
    )

    portfolio = PortfolioManager()
    shop = ShopManager()

    class Meta:
        unique_together = ("key", "parent")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self) -> str:
        return self.name
