# Generated by Django 4.0.4 on 2022-05-26 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_tags_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='title',
            new_name='post_title',
        ),
    ]
