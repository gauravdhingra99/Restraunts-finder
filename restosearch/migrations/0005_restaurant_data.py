# Generated by Django 2.2.1 on 2019-05-07 17:46

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restosearch', '0004_delete_worldborder'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
