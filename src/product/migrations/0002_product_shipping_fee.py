# Generated by Django 3.0.1 on 2019-12-23 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shipping_fee',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
