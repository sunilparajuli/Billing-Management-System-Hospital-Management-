# Generated by Django 2.2.2 on 2021-02-23 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('products', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calllog',
            name='fk_store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Store'),
        ),
        migrations.AddField(
            model_name='calllog',
            name='fk_variation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Variation'),
        ),
    ]
