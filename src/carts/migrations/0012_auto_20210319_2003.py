# Generated by Django 2.2.2 on 2021-03-19 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0011_auto_20210317_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='fk_cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='carts.Cart'),
        ),
    ]
