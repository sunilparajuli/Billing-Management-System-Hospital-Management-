# Generated by Django 2.2.2 on 2021-02-28 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='appointment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='remarks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
