# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accreditations', '0009_auto_20170522_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accreditedparty',
            name='dcp_host',
            field=models.CharField(default='dcp-for-this-party.testpoint.io', max_length=2048, unique=True),
        ),
    ]
