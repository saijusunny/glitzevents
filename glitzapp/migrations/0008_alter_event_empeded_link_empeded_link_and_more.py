# Generated by Django 4.0.2 on 2023-11-15 04:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitzapp', '0007_alter_event_empeded_link_empeded_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_empeded_link',
            name='empeded_link',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='events_table',
            name='posting_date',
            field=models.DateField(default=datetime.date(2023, 11, 15)),
        ),
    ]
