# Generated by Django 4.1.5 on 2023-01-07 02:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('first_name', models.TextField()),
                ('last_name', models.TextField(blank=True, default='', null=True)),
                ('username', models.TextField(blank=True, default=None, null=True)),
                ('reg_date', models.DateTimeField(default=datetime.datetime(2023, 1, 7, 5, 16, 49, 839332))),
                ('dialog', models.TextField(default='start')),
                ('temp', models.TextField(blank=True, default='')),
            ],
        ),
    ]