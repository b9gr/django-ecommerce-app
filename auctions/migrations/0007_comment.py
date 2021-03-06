# Generated by Django 3.2.6 on 2021-09-29 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=128)),
                ('commentedListing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listingcomments', to='auctions.auctionlistings')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercomments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
