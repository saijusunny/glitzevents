# Generated by Django 4.0.2 on 2023-08-25 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glitzapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_registration',
            old_name='name',
            new_name='firstname',
        ),
        migrations.RemoveField(
            model_name='user_registration',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user_registration',
            name='nickname',
        ),
        migrations.AlterField(
            model_name='user_registration',
            name='pro_pic',
            field=models.ImageField(default='static/images/logo/icon.png', upload_to='images/propic'),
        ),
    ]