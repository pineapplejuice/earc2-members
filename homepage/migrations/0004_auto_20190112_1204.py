# Generated by Django 2.0.5 on 2019-01-12 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_announcement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='expiration_date',
        ),
        migrations.AlterField(
            model_name='announcement',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]