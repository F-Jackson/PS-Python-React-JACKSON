# Generated by Django 4.1.4 on 2022-12-22 01:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userhistorycallmodel_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhistorycallmodel',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 22, 1, 24, 47, 266906, tzinfo=datetime.timezone.utc)),
        ),
    ]
