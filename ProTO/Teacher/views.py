from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from rest_framework import status
from .models import StudentInClassRoom

# Create your views here.

def reg_teacher(request):
    obj=StudentInClassRoom.objects.get(pk=3)
    print(obj.classId,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    return HttpResponse (f'DONE {obj.student.username}')
