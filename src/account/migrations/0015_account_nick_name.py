# Generated by Django 2.2.2 on 2021-01-05 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_account_firebase_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='nick_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]