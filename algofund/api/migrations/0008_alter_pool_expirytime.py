# Generated by Django 4.0.5 on 2022-06-18 15:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_pool_expirytime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='expiryTime',
            field=models.DateField(default=datetime.datetime(2022, 6, 19, 15, 1, 58, 152945)),
        ),
    ]
