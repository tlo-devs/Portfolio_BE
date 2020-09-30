from django.db import migrations
from django.conf import settings
from django.contrib.auth import get_user_model


def add_admin(apps, schema_editor):
    model = get_user_model()
    if settings.DEBUG:
        model.objects.create_superuser(
            email="tester@tester.de",
            password="example"
        )
    else:
        model.objects.create_superuser(
            email=settings.PROD_ADMIN_EMAIL,
            password=settings.PROD_ADMIN_PASSWORD
        )


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_admin)
    ]
