# Generated by Django 3.0.6 on 2020-06-03 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200603_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inches',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
