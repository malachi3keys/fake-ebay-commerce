# Generated by Django 4.0.4 on 2022-05-26 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_user_id_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_tag', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='listing',
            name='category_tag',
        ),
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.URLField(blank=True),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ManyToManyField(blank=True, related_name='watchlisting', to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watcher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replyuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dollar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_listing', to='auctions.listing')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='list_tag',
            field=models.ManyToManyField(related_name='category', to='auctions.tags'),
        ),
    ]
