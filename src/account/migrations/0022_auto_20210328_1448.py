# Generated by Django 2.2.2 on 2021-03-28 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20210322_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='fk_doctor_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors_assigned', to=settings.AUTH_USER_MODEL),
        ),
    ]