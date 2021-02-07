# Generated by Django 2.2.2 on 2021-02-06 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20210112_1912'),
        ('account', '0019_auto_20210129_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='calllog',
            name='fk_staff_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='calllog',
            name='fk_variation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Variation'),
        ),
        migrations.AddField(
            model_name='calllog',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='calllog',
            name='staff_entry_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]