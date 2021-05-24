from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from rest_framework import status
from .models import StudentInClassRoom
from django.contrib.auth.models import auth, User
from Teacher.models import TEACHER, TeacherClassRoom
from .forms import ClassRoomForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes
from django.db import IntegrityError


# Create your views here.

def reg_teacher(request):
    if request.user.is_authenticated == False:
        return redirect('/')

    if request.method == 'GET':
        try:
            new_teacher = User.objects.get(username=request.user.username)
            Teacher_obj = TEACHER.objects.get(teacher=new_teacher)

            # print(Teacher_obj.is_active)
        except Exception as e:
            Teacher_obj = None
            messages.info(request, "Your Request is Registered Waiting for admin review")
            TEACHER.objects.create(teacher=new_teacher, is_active=False)
            return render(request, 'teacherReg.html')
        if Teacher_obj.is_active:
            messages.info(request, "You are Teacher Already")
        else:
            messages.info(request, "Your Request is Registered Waiting for admin review")

    return render(request, 'teacherReg.html')


def new_class(request):
    if request.method == 'GET':
        form = ClassRoomForm()
        return render(request, 'classRoom.html', {"form": form})

    if request.method == "POST":
        form = ClassRoomForm(data=request.POST)

        if form.is_valid():
            try:
                new_form = form.save(commit=False)
                new_form.teacher = TEACHER.objects.get(pk=request.user)
                new_form.classRoomName = form.cleaned_data['classRoomName']
                new_form.save()
                # temp_class=TeacherClassRoom.objects.get(pk=new_form.id)
                url_enode = urlsafe_base64_encode(force_bytes(new_form.id))
                new_form.class_url = url_enode
                new_form.save()
                return HttpResponse(f"url to the class room is {url_enode}")
            except IntegrityError as e:
                return HttpResponse("Class Name Already Exist Please change the Name ")
        else:
            return HttpResponse("Some Issue Try again later !")


def join_class(request):
    return HttpResponse("HHH")
