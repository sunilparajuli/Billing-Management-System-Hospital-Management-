# Generated by Django 2.2.2 on 2021-03-17 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0010_cart_fk_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='tax_percentage',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=10),
        ),
    ]
