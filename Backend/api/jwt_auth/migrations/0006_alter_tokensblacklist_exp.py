# Generated by Django 4.1.3 on 2022-12-02 21:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0005_alter_tokensblacklist_exp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokensblacklist',
            name='exp',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 2, 21, 52, 35, 961181, tzinfo=datetime.timezone.utc)),
        ),
    ]