# Generated by Django 2.2.2 on 2021-03-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20210314_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=25),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='discount_percent',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=25),
        ),
    ]
