# Generated by Django 3.2.1 on 2021-05-24 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0006_alter_studentinclassroom_unique_together'),
        ('Event', '0003_alter_event_room'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('eventname', 'Room')},
        ),
    ]
