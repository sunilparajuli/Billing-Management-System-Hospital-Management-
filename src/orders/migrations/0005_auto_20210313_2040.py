# Generated by Django 2.2.2 on 2021-03-13 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210313_2036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseitem',
            old_name='purchase',
            new_name='fk_purchase',
        ),
    ]
