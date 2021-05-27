from django.contrib import admin
from .models import TEACHER,TeacherClassRoom,StudentInClassRoom
from django.contrib.auth.models import User
# Register your models here.



class Teacher_admin(admin.ModelAdmin):
    model = TEACHER
    list_filter  = ('teacher',)
    search_fields=('teacher',)

class ClassRoom_admin(admin.ModelAdmin):
    model=TeacherClassRoom
    list_filter = ('teacher','classRoomName')
    search_fields = ('teacher','classRoomName')
    list_display = ('teacher','classRoomName','id')

class Student_in_admin(admin.ModelAdmin):
    model=StudentInClassRoom
    list_filter = ('classId', 'student')
    search_fields = ('classId', 'student')
    list_display = ('classId', 'student', 'id')

admin.site.register(TEACHER,Teacher_admin)

admin.site.register(TeacherClassRoom,ClassRoom_admin)
admin.site.register(StudentInClassRoom,Student_in_admin)