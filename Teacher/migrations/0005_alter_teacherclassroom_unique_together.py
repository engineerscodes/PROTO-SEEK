# Generated by Django 3.2.1 on 2021-05-23 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0004_studentinclassroom'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teacherclassroom',
            unique_together={('teacher', 'classRoomName')},
        ),
    ]