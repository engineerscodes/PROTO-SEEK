from django.db import models
from django.contrib.auth.models import User


class TEACHER(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return "EMAIL: " + self.teacher.email + " | USERNAME: " + self.teacher.username

class TeacherClassRoom(models.Model):
    class Meta:
        unique_together = (('teacher', 'classRoomName'))
    teacher=models.ForeignKey(TEACHER,on_delete=models.CASCADE)
    classRoomName=models.CharField(max_length=25)
    class_url=models.CharField(max_length=2000,blank=True)

    def __str__(self):
        return  str(self.id)

class StudentInClassRoom(models.Model):
    class Meta:
        unique_together = (('classId', 'student'))
    classId=models.ForeignKey(TeacherClassRoom,on_delete=models.CASCADE,to_field='id')
    student=models.ForeignKey(User,on_delete=models.CASCADE)

