from django.db import migrations
from ..models import CategoryTree


def add_category_defaults(apps, schema_editor):
    # Root Nodes
    portfolio_root = CategoryTree.objects.create(name="Portfolio", key="portfolio")
    shop_root = CategoryTree.objects.create(name="Shop", key="shop")
    portfolio_root.save()
    shop_root.save()

    # Portfolio 1st Level Leaves
    leaves = (
                 {"name": "Alles", "key": "all", "parent": portfolio_root},
                 {"name": "Bilder", "key": "image", "parent": portfolio_root},
                 {"name": "Videos", "key": "video", "parent": portfolio_root},
    )
    first_level = {leaf.get("key"): CategoryTree.objects.create(**leaf) for leaf in leaves}
    for node in first_level.values():
        node.save()

    # Portfolio 2nd Level Leaves
    # IMG
    leaves = (
                 {"name": "Alles", "key": "all", "parent": first_level.get("image")},
                 {"name": "Landschaft", "key": "landscape", "parent": first_level.get("image")},
                 {"name": "Architektur", "key": "architecture", "parent": first_level.get("image")},
                 {"name": "Portraits", "key": "portrait", "parent": first_level.get("image")},
    )
    [CategoryTree.objects.create(**leaf).save() for leaf in leaves]

    # VID
    leaves = (
                 {"name": "Alles", "key": "all", "parent": first_level.get("video")},
                 {"name": "Imagevideos", "key": "imagevideo", "parent": first_level.get("video")},
                 {"name": "Aftermovie", "key": "aftermovie", "parent": first_level.get("video")},
                 {"name": "Kurzfilme", "key": "shortmovie", "parent": first_level.get("video")},
                 {"name": "Musikvideos", "key": "musicvideo", "parent": first_level.get("video")},
    )
    [CategoryTree.objects.create(**leaf).save() for leaf in leaves]

    # Shop 1st Level Leaves
    leaves = (
                 {"name": "Alles", "key": "all", "parent": shop_root},
                 {"name": "Digital", "key": "digital", "parent": shop_root},
    )
    first_level = {leaf.get("key"): CategoryTree.objects.create(**leaf) for leaf in leaves}
    for node in first_level.values():
        node.save()

    # Shop 2nd Level Leaves
    # LUT
    leaves = (
                 {"name": "Alles", "key": "all", "parent": first_level.get("digital")},
                 {"name": "LUTs", "key": "lut", "parent": first_level.get("digital")},
                 {"name": "Presets", "key": "preset", "parent": first_level.get("digital")},
    )
    [CategoryTree.objects.create(**leaf).save() for leaf in leaves]

    portfolio_root.refresh_from_db()
    shop_root.refresh_from_db()
    CategoryTree.objects.rebuild()


class Migration(migrations.Migration):
    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_category_defaults)
    ]
