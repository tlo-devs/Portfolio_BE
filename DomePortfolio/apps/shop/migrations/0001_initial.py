# Generated by Django 3.1 on 2020-08-23 14:46

import DomePortfolio.lib.storage.gcp_storage.storage
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(storage=DomePortfolio.lib.storage.gcp_storage.storage.GCPStorage(), upload_to='')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar')], default='EUR', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='EUR', max_digits=19)),
                ('sale', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('description', models.TextField()),
                ('download', models.FileField(storage=DomePortfolio.lib.storage.gcp_storage.storage.GCPStorage(), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_on', models.DateTimeField()),
                ('ordered_by', models.EmailField(max_length=254)),
                ('amount_paid_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar')], default='EUR', editable=False, max_length=3)),
                ('amount_paid', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='EUR', max_digits=19)),
                ('purchased_with_sale', models.PositiveSmallIntegerField(default=0)),
                ('product_downloads_remaining', models.PositiveSmallIntegerField()),
                ('download_expires_on', models.DateTimeField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='shop.item')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_field', models.PositiveSmallIntegerField(default=0)),
                ('image', imagekit.models.fields.ProcessedImageField(storage=DomePortfolio.lib.storage.gcp_storage.storage.GCPStorage(), upload_to='')),
                ('image_after', imagekit.models.fields.ProcessedImageField(storage=DomePortfolio.lib.storage.gcp_storage.storage.GCPStorage(), upload_to='')),
                ('parent_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.item')),
            ],
            options={
                'ordering': ['order_field'],
                'abstract': False,
            },
        ),
    ]
