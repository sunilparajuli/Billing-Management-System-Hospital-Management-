# Generated by Django 2.2.2 on 2020-06-01 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('carts', '0004_auto_20200601_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='fk_payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_ordered_store', to='payment.PaymentMethod'),
        ),
    ]