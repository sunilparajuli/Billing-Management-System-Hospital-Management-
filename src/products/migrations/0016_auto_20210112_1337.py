# Generated by Django 2.2.2 on 2021-01-12 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20210112_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_internal',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='variation',
            name='is_internal',
            field=models.BooleanField(default=False),
        ),
    ]