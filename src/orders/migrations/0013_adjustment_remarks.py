# Generated by Django 2.2.2 on 2021-03-26 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_adjustment'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjustment',
            name='remarks',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]