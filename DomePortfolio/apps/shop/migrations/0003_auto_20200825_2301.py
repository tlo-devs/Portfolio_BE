# Generated by Django 3.1 on 2020-08-25 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200825_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='open',
        ),
        migrations.AddField(
            model_name='order',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
