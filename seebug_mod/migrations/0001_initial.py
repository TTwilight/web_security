# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-16 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='seebug',
            fields=[
                ('SSV_ID', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('Push_time', models.CharField(max_length=20)),
                ('Level', models.CharField(max_length=20)),
                ('Poc_name', models.CharField(max_length=200)),
                ('Detail_link', models.CharField(max_length=100)),
                ('Has_cve', models.CharField(max_length=20)),
                ('Has_poc', models.CharField(max_length=20)),
                ('Has_target', models.CharField(max_length=20)),
                ('Has_detail', models.CharField(max_length=20)),
                ('Has_chart', models.CharField(max_length=20)),
            ],
        ),
    ]
