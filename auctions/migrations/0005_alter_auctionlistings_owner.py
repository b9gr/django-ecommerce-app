# Generated by Django 3.2.6 on 2021-09-25 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_price_auctionlistings_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='auction', to=settings.AUTH_USER_MODEL),
        ),
    ]
