# Generated by Django 3.1 on 2020-08-30 07:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('completed', models.BooleanField(default=False)),
                ('related_paypal_order', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('ordered_on', models.DateTimeField(null=True)),
                ('customer_email', models.EmailField(max_length=254, null=True)),
                ('customer_id', models.CharField(max_length=100, null=True)),
                ('purchased_with_sale', models.PositiveSmallIntegerField(default=0)),
                ('product_downloads_remaining', models.PositiveSmallIntegerField(null=True)),
                ('download_expires_on', models.DateTimeField(null=True)),
                ('product_download', models.URLField(null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='shop.item')),
            ],
        ),
    ]