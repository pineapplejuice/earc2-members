# Generated by Django 2.0.5 on 2018-06-03 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_members', '0007_auto_20180529_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='app_type',
        ),
    ]
