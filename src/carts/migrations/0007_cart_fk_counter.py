# Generated by Django 2.2.2 on 2021-03-04 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0001_initial'),
        ('carts', '0006_remove_cart_fk_delivery_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='fk_counter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='counter.Counter'),
        ),
    ]
