# Generated by Django 4.0.4 on 2022-05-26 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_tags_remove_listing_category_tag_alter_listing_img_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]
