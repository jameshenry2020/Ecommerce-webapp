# Generated by Django 3.0.1 on 2020-01-25 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_order_shipping_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='being_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='received',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='1233', max_length=20),
            preserve_default=False,
        ),
    ]
