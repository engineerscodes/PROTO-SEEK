# Generated by Django 3.2.1 on 2021-05-23 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0002_teacherclassroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherclassroom',
            name='classRoomName',
            field=models.CharField(max_length=25),
        ),
    ]
