# Generated by Django 2.1.5 on 2019-05-09 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_members', '0016_auto_20190218_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, verbose_name='My license expires'),
        ),
    ]
