# Generated by Django 3.2.1 on 2021-05-23 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='Room',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]