# Generated by Django 2.2.2 on 2021-03-05 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_variationbatch_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='variationbatch',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]