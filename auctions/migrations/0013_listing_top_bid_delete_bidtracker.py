# Generated by Django 4.0.4 on 2022-06-20 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_rename_bidtable_bidtracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='top_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='BidTracker',
        ),
    ]