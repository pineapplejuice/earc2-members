# Generated by Django 2.1.5 on 2019-04-29 08:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0012_auto_20190428_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='expiration_date',
            field=models.DateTimeField(blank=True, default=datetime.date(2019, 12, 31)),
            preserve_default=False,
        ),
    ]