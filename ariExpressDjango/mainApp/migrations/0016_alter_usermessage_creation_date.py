# Generated by Django 4.2.1 on 2023-05-14 07:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0015_alter_usermessage_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessage',
            name='creation_date',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
    ]