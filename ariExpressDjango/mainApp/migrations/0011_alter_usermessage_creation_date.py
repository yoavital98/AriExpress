# Generated by Django 4.2.1 on 2023-05-13 20:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0010_create_usermessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessage',
            name='creation_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 5, 13, 20, 10, 43, 215480, tzinfo=datetime.timezone.utc)),
        ),
    ]
