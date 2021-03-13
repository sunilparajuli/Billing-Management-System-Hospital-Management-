# Generated by Django 2.2.2 on 2021-03-13 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210313_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='purchaseitems',
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='fk_purchase',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchaseitems', to='orders.Purchase'),
        ),
    ]
