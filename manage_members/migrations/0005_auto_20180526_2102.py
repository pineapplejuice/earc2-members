# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-27 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_members', '0004_auto_20180526_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='expiration_date',
            field=models.DateField(verbose_name='My license expires'),
        ),
    ]
