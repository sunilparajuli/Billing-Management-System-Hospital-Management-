# Generated by Django 2.2.2 on 2021-03-01 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_variationbatchprice_fk_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variationbatchprice',
            name='fk_user_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.UserTypes'),
        ),
        migrations.AlterField(
            model_name='variationprice',
            name='fk_user_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.UserTypes'),
        ),
    ]
