# Generated by Django 2.1.5 on 2019-04-01 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_event_event_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='meeting_place',
        ),
        migrations.DeleteModel(
            name='Meeting',
        ),
    ]
