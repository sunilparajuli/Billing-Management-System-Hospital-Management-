# Generated by Django 2.2.2 on 2020-08-08 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_storewiseorder_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='storewiseorder',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='storewiseorder',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]