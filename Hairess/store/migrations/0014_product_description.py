# Generated by Django 3.0.6 on 2020-06-11 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
