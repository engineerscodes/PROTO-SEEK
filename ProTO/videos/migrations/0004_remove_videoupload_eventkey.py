# Generated by Django 3.2.1 on 2021-05-25 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_videoupload_eventkey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoupload',
            name='Eventkey',
        ),
    ]
