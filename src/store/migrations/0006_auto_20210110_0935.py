# Generated by Django 2.2.2 on 2021-01-10 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_storeaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeaccount',
            name='fk_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
