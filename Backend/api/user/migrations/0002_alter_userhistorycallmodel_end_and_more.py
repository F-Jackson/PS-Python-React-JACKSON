# Generated by Django 4.1.4 on 2022-12-21 22:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhistorycallmodel',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userhistorycallmodel',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 22, 56, 47, 210131, tzinfo=datetime.timezone.utc)),
        ),
    ]
