# Generated by Django 4.0.4 on 2022-06-07 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='images/'),
        ),
    ]