# Generated by Django 2.2.2 on 2021-04-06 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('account', '0024_visittype_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='fk_user_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.UserTypes'),
        ),
    ]
