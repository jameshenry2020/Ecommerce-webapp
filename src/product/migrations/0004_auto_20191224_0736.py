# Generated by Django 3.0.1 on 2019-12-24 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20191223_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shipping_fee',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='shipping_fee',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
