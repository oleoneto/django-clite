# Generated by Django 2.1 on 2018-10-30 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_track_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['title']},
        ),
        migrations.RemoveField(
            model_name='album',
            name='release_date',
        ),
    ]
