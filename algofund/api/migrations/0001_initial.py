# Generated by Django 4.0.5 on 2022-06-05 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=200)),
                ('applicationIndex', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='pools')),
            ],
        ),
    ]