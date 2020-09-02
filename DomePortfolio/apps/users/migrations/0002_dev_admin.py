from django.db import migrations
from django.conf import settings
from django.contrib.auth import get_user_model


def add_dev_admin(apps, schema_editor):
    if settings.DEBUG:
        model = get_user_model()
        model.objects.create_superuser(
            email="tester@tester.de",
            password="example"
        )


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_dev_admin)
    ]
