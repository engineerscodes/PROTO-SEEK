# Generated by Django 3.2.1 on 2021-05-24 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoupload',
            name='Eventkey',
        ),
    ]