# Generated by Django 4.0.2 on 2023-11-14 14:54

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glitzapp', '0006_alter_events_table_posting_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_empeded_link',
            name='empeded_link',
            field=embed_video.fields.EmbedVideoField(default=1),
            preserve_default=False,
        ),
    ]
