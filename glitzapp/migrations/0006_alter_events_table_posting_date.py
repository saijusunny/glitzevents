# Generated by Django 4.0.2 on 2023-11-14 07:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitzapp', '0005_events_table_event_social_event_images_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events_table',
            name='posting_date',
            field=models.DateField(default=datetime.date(2023, 11, 14)),
        ),
    ]