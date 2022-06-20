# Generated by Django 4.0.5 on 2022-06-18 13:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_fund_applicationindex_alter_pool_expirytime'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundWithdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requesterMnemonic', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='pool',
            name='expiryTime',
            field=models.DateField(default=datetime.datetime(2022, 6, 19, 13, 6, 0, 322565)),
        ),
    ]