from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class RootQueryset(models.QuerySet):
    root_key: str

    def get_parent_leaves(self, parent_key: str) -> models.QuerySet:
        leaves = [
            l for l in self.filter(
                children__isnull=True
            ) if l.get_root().key == self.root_key
                 and l.key != "all"
                 and l.parent.key == parent_key
        ]
        return self.filter(id__in=[node.id for node in leaves])

    def all(self):
        root_id = self.all()
        return


class PortfolioRootQueryset(RootQueryset):
    root_key = "portfolio"


class ShopRootQueryset(RootQueryset):
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

    portfolio = PortfolioRootQueryset.as_manager()
    shop = ShopRootQueryset.as_manager()

    class Meta:
        unique_together = ("key", "parent")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self) -> str:
        return self.name
