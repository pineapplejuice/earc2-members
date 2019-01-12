# Generated by Django 2.0.5 on 2019-01-12 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_members', '0011_auto_20180605_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='license_type',
            field=models.CharField(choices=[('T', 'Technician'), ('G', 'General'), ('A', 'Advanced'), ('E', 'Amateur Extra')], max_length=1),
        ),
    ]
