# Generated by Django 3.0.1 on 2019-12-24 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20191224_0736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='shipping_fee',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_fee',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
