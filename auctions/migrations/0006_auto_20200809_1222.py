# Generated by Django 3.0.8 on 2020-08-09 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200809_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='bidder',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='listings',
            name='creator',
            field=models.CharField(max_length=32),
        ),
    ]
