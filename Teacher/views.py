from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from rest_framework import status
from .models import StudentInClassRoom
from django.contrib.auth.models import auth, User
from Teacher.models import TEACHER, TeacherClassRoom, StudentInClassRoom
from .forms import ClassRoomForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes
from django.db import IntegrityError

from Event.models import Event


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
                return render(request,'gallery2.html',{'code':url_enode})
                #return HttpResponse(f"CLASS CODE IS {url_enode} and urls is teacher/class/{url_enode}")
            except IntegrityError as e:
                alclass=TeacherClassRoom.objects.get(teacher=TEACHER.objects.get(pk=request.user),classRoomName= form.cleaned_data['classRoomName'])
                messages.info(request,"Class Name Already Exist  Please change the Name")
                return render(request, 'gallery.html', {'code': alclass})
                #return HttpResponse("Class Name Already Exist Please change the Name ")
        else:
            #return HttpResponse("Some Issue Try again later !")
            messages.info(request, "Some Issue Try again later !")
            return render(request, 'gallery.html', {'code': None})



def join_class(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == "GET":
        return render(request, 'joinClass.html')

    if request.method == 'POST':

        ClassCode = request.POST['class_code']

        try:
            Cl_id = force_text(urlsafe_base64_decode(ClassCode))
            temT = TeacherClassRoom.objects.get(pk=Cl_id)
            try :
                if temT.teacher==TEACHER.objects.get(pk=request.user) :
                    messages.info(request, 'You cannot join Your Class !! Becasue You Create It')
                    return redirect('/teacher/join/')
            except Exception as e :
                 pass
            StudentInClassRoom.objects.create(classId=temT, student=User.objects.get(username=request.user.username))
            messages.info(request,f'Joined New Class {temT.classRoomName}')
        except IntegrityError as e:
            messages.info(request,"YOUR HAVE ALREADY JOINDED THE CLASS !!")
        except Exception as e:
           print(e)
           messages.info(request,'INVALID CLASS CODE !!')

        return  redirect('/teacher/join/')


def view_class(request, cl_id):
    if request.method=='GET':
        try:
            get_class=TeacherClassRoom.objects.get(class_url=cl_id)
            teach=TEACHER.objects.get(pk=request.user)
            if get_class.teacher==teach:
                get_students=StudentInClassRoom.objects.filter(classId=get_class.id)
                Event_rec=Event.objects.filter(Room=get_class.id)
                event_count=Event_rec.count()

                return render(request,'class_student.html',{'clsName':get_class.classRoomName,
                                     'students':get_students,'Events':Event_rec,'Count':event_count})
            else:
                return redirect('/')
        except Exception as e:
            #print(e)
            #return HttpResponse("CLASS DON'T EXIST")
            messages.info(request,"CLASS DON'T EXIST!! ")
            return redirect('/teacher/join/')



