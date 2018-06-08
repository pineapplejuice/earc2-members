# Generated by Django 2.0.5 on 2018-06-08 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('event_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('event_venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.MeetingPlace')),
            ],
        ),
    ]
