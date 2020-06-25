# Generated by Django 3.0.6 on 2020-06-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_shippingprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shippingprice',
        ),
        migrations.AddField(
            model_name='order',
            name='shippingprice',
            field=models.IntegerField(default=0),
        ),
    ]