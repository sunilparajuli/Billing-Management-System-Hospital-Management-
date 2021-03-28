# Generated by Django 2.2.2 on 2021-03-28 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20210326_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjustment',
            name='change_quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='adjustment',
            name='final_quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='adjustment',
            name='initial_quantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]