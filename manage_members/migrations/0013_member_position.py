# Generated by Django 2.0.5 on 2019-01-14 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_members', '0012_auto_20190112_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='position',
            field=models.CharField(blank=True, choices=[('PR', 'President'), ('VP', 'Vice-President'), ('SE', 'Secretary'), ('TR', 'Treasurer'), ('DI', 'Director')], max_length=2),
        ),
    ]
