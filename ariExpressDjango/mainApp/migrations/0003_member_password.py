# Generated by Django 4.2 on 2023-05-08 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_alter_cart_baskets'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='password',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
