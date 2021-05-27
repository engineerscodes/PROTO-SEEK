from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import status
from django.http import HttpResponse
# Create your views here.
from django.apps import apps
from .forms import vd_form
from rest_framework.views import APIView
from .models import videoUpload, Marks
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .serializers import videoUploadSerializer, MarksSerializer, SubmitVideo, VDContent, EventSerial, videoUploadSerializerMark
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from datetime import date
from django.utils.encoding import force_text, force_bytes
from Teacher.models import StudentInClassRoom, TeacherClassRoom, TEACHER
from rest_framework.decorators import api_view

Mode = apps.get_model('Moderator', 'Mode')
Events = apps.get_model('Event', 'Event')


def homepage(request):
    # return HttpResponse(request.user.username)

    if request.method == 'GET':

        try:
            is_teacher = TEACHER.objects.get(teacher=request.user)
            if is_teacher.is_active:
                all_classes = TeacherClassRoom.objects.filter(teacher=is_teacher)
                #print(all_classes.values_list('id'))
                all_events=Events.objects.filter(Room__in=all_classes.values_list('id'))
                #print(all_events.values_list('id'))
                all_video=videoUpload.objects.filter(EventID__in=all_events.values_list('id'))
                #print(all_video)
            else:
                return HttpResponse("Your Request Is Pending for Admin review")
        except Exception as e:
            print(e)
            #return HttpResponse("Your Not Teacher Plz Contact your Admin")
            return redirect('/student/')

    return render(request, 'AllClass.html', {'classes': all_classes,'videos':all_video})


def Home_student(request):
    if not request.user.is_authenticated:
        return redirect('/account/login')
    if request.method == "GET":

        try:
            is_Student = StudentInClassRoom.objects.filter(student=request.user)
            All_List=is_Student.values_list('classId')
            teacher_room = TeacherClassRoom.objects.filter(pk__in=All_List)
            #print(teacher_room)
        except Exception as e:

            return HttpResponse("Check your email")
        Zipped=zip(is_Student,teacher_room)
    return render(request, 'student.html', {'classes': Zipped})


def get_class(request, cl_name, cl_id):
    if not request.user.is_authenticated:
        return redirect('/account/login')
    if request.method == "GET":
        try:
            is_Student = StudentInClassRoom.objects.get(pk=cl_id)
            print(request.user,is_Student.student,is_Student.classId,cl_name)
            if request.user == is_Student.student and str(is_Student.classId) == cl_name:
                print(TeacherClassRoom.objects.get(pk=cl_name),'$$$$$$$$$$$$$$$')
                #class_event=Events.objects.get(Room=cl_name)
                #print(class_event)
                return redirect('/upload/')
            else:
                #return HttpResponse("You cannot Access this Class")
                messages.info(request,'You cannot Access this Class')
                return redirect('/teacher/join/')
        except Exception as e:
            print(e)
            #return HttpResponse("No SUCH CLASS ROOM EXIST")
            messages.info(request, 'No SUCH CLASS ROOM EXIST')
            return redirect('/teacher/join/')




def upload_file(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect('/account/login')

        form = vd_form()
        student_in_class = StudentInClassRoom.objects.filter(student=request.user)
        class_id_list = student_in_class.values_list('classId')
        teacher_room = TeacherClassRoom.objects.filter(pk__in=class_id_list)
        teacher_room_id_list = teacher_room.values_list('id')
        print(teacher_room)
        event = Events.objects.filter(Room__in=teacher_room_id_list)
        # print(event)

        return render(request, "upload.html", {"form": form, "event": event})
    else:
        return redirect('/account/login')


class ajaxsubmitVideo(APIView):
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]

    def post(self, request, format=None):

        user = request.user
        if (user.is_authenticated):
            serializerss = SubmitVideo(data=request.data)
            # print(request.POST.get('captions'))

            if serializerss.is_valid():
                # print(serializerss.validated_data[''])
                # print(request.POST['events'])
                form = vd_form(data=request.POST, files=request.FILES)
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.username = request.user.email
                    new_form.date = date.today().strftime('%Y-%m-%d')
                    new_form.save()
                    video = videoUpload.objects.get(pk=new_form.id)
                    video.url_64encoding = urlsafe_base64_encode(force_bytes(new_form.id))
                    video.thumbnail = serializerss.validated_data['thumbnail']
                    video.EventID=request.POST['events']
                    try:
                        video.EventName = Events.objects.get(pk=request.POST['events']).eventname
                        video.save()
                    except Exception as e:
                        return Response(data="Event doesnot exist", status=status.HTTP_400_BAD_REQUEST)
                    # serializerss.save(username=request.user.email,date= date.today().strftime('%Y-%m-%d'))
                    # print(videoUpload.objects.filter(pk=serializerss))
                return Response("VIDEO SUMBITTED", status=status.HTTP_200_OK)
            else:
                return Response(serializerss.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="access denied", status=status.HTTP_400_BAD_REQUEST)


def getSingleVideo(request, uuid):
    if (request.user.is_authenticated == False):
        return redirect('/account/login')
    try:
        is_teacher = TEACHER.objects.get(teacher=request.user)
        if not is_teacher.is_active:
            #return HttpResponse("Your Request Is Pending for Admin review")
            messages.info(request,'Your Request Is Pending for Admin review')
            return redirect('/teacher/')
    except Exception as e:
        return HttpResponse("Your Not Teacher Plz Contact your Admin")


    if request.method == 'GET':
        try:
            id = force_text(urlsafe_base64_decode(uuid))
            video = videoUpload.objects.get(pk=id)

            event_trg = Events.objects.get(pk=video.EventID)
            #print(event_trg.Room)
            temp=event_trg.Room
            #print(str(temp),)
            Is_teacher_room=TeacherClassRoom.objects.get(pk=str(temp))
            print(Is_teacher_room.teacher)
            if  not Is_teacher_room.teacher==TEACHER.objects.get(pk=request.user) :
                 #return HttpResponse('No Access')
                 return render(request,'Noacess.html',{'text':"NO ACCESS",'i':'You cannot view this video file!!'})
        except Exception as e:
            video = None
            #return HttpResponse("Video Doesnot Exist")
            return render(request, 'Noacess.html', {'text': "NOT FOUND", 'i': 'VIDEO DOESNOT EXIST!!'})

        if video is not None:
            try:
                current_video_marks = Marks.objects.filter(videoId=id)
                return render(request, 'video.html', {'data': video, 'MODES': True, 'Marks': current_video_marks})
            except Exception:
                return redirect('/videos/')

        else:
            return redirect('/videos/')

    if request.method == 'POST':
        try:
            id_post = force_text(urlsafe_base64_decode(uuid))
            video_post = videoUpload.objects.get(pk=id_post)
        except Exception:
            video_post = None
        if request.POST['video_marks'] == '':
            return redirect(f'/videos/{uuid}')
        try:
            neg = int(request.POST['video_marks'])
            if neg < 0:
                messages.info(request, "MARKS CANNOT BE LESS THAN ZERO")
                return redirect(f'/videos/{uuid}')
        except ValueError:
            messages.info(request, "NO STRING ALLOWED")
            return redirect(f'/videos/{uuid}')
        if video_post != None and request.POST['video_marks'] != '':
            try:
                check_marks = Marks.objects.get(videoId=id_post, moderator_email=request.user.email)
                # print(video_post.total_marks())

            except Exception:
                check_marks = None
            if check_marks is not None and neg >= 0:
                # print(neg,'$$$$$$$$$$$$$$$$',check_marks.marks)
                video_post.Total_marks = int(video_post.Total_marks) + (int(-check_marks.marks) + neg)
                # print(video_post.total_marks(),"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",video_post.Total_marks)
                video_post.save()
                check_marks.marks = request.POST['video_marks']
                check_marks.date = date.today().strftime('%Y-%m-%d')
                check_marks.save()
                return redirect(f'/videos/{uuid}')
            if check_marks is None and neg >= 0:
                video_post.Total_marks = int(video_post.Total_marks) + neg
                # print(video_post.total_marks(),"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                video_post.save()
                video_marks = Marks()

                video_marks.videoId = id_post
                video_marks.video_link = uuid
                video_marks.by_email = video_post.username

                video_marks.moderator_email = request.user.email
                video_marks.date = date.today().strftime('%Y-%m-%d')
                video_marks.marks = request.POST['video_marks']
                video_marks.EventName = video_post.EventName
                video_marks.verfiyed = True
                video_marks.save()
                return redirect(f'/videos/{uuid}')
        else:
            return redirect('/videos/')


def allVideos_of_class(request):

   return redirect('/')

@api_view(['GET'])
def getcontent(request):

    if request.method =='GET':
        if request.is_ajax() and request.user.is_authenticated:
            try:
                is_teacher = TEACHER.objects.get(teacher=request.user)
                if is_teacher.is_active:
                    all_classes = TeacherClassRoom.objects.filter(teacher=is_teacher)
                    # print(all_classes.values_list('id'))
                    all_events = Events.objects.filter(Room__in=all_classes.values_list('id'))
                    # print(all_events.values_list('id'))
                    all_video = videoUpload.objects.filter(EventID__in=all_events.values_list('id'),Total_marks=0)
                    # print(all_video)
                else:
                    return HttpResponse("Your Request Is Pending for Admin review")
            except Exception as e:
                return HttpResponse("Your Not Teacher Plz Contact your Admin")
            try :
              index=int(request.GET.get('vdreq'))
            except:
                return Response("EXCEPTION HAPPENDED", status=status.HTTP_400_BAD_REQUEST)
            #Total=videoUpload.objects.all().count()
            #print(Total)
            #print(index*6)
            allcontent =  all_video.reverse()[6*(index-1):6*index]
            videofile= VDContent(allcontent,many=True)
            return Response({"data":videofile.data})
        else :
            return Response("PLZ AUTHENTICATE AND CALL MUST BE AJAX", status=status.HTTP_400_BAD_REQUEST)


def classesInof(request):

    if request.method =='GET':
        try:
            is_teacher = TEACHER.objects.get(teacher=request.user)
            if is_teacher.is_active:
                all_classes = TeacherClassRoom.objects.filter(teacher=is_teacher)
                # print(all_classes.values_list('id'))
                all_events = Events.objects.filter(Room__in=all_classes.values_list('id'))
                # print(all_events.values_list('id'))
                pending_video = videoUpload.objects.filter(EventID__in=all_events.values_list('id'), Total_marks=0)
                correctVideo=videoUpload.objects.filter(EventID__in=all_events.values_list('id'), Total_marks__gt=0)
                # print(all_video)
            else:
                #return HttpResponse("Your Request Is Pending for Admin review")
                messages.info("Your Request Is Pending for Admin review")
                return redirect('/teacher/')
        except Exception as e:
            return HttpResponse("Your Not Teacher Plz Contact your Admin")
    return render(request, 'info.html', {'marks': correctVideo, 'LeftOver':pending_video })


@api_view(['GET'])
def analaytics(request):
    if request.method == 'GET':

        if request.method == 'GET':
            try:
                is_teacher = TEACHER.objects.get(teacher=request.user)
                if is_teacher.is_active:
                    all_classes = TeacherClassRoom.objects.filter(teacher=is_teacher)
                    # print(all_classes.values_list('id'))
                    all_events = Events.objects.filter(Room__in=all_classes.values_list('id'))
                    # print(all_events.values_list('id'))
                    pending_video = videoUpload.objects.filter(EventID__in=all_events.values_list('id'), Total_marks=0).count()
                    correctVideo = videoUpload.objects.filter(EventID__in=all_events.values_list('id'),
                                                              Total_marks__gt=0).count()
                    # print(all_video)
                else:
                    return HttpResponse("Your Request Is Pending for Admin review")
            except Exception as e:
                return HttpResponse("Your Not Teacher Plz Contact your Admin")
            if request.is_ajax():
                return Response({"Left_count":pending_video,"Actual_corrected":correctVideo })

        else :
            return Response ({"data":"Acess DENIED "},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ajaxModeration(request):
    if request.method == 'GET':
        try:
            is_teacher = TEACHER.objects.get(teacher=request.user)
            if is_teacher.is_active:
                all_classes = TeacherClassRoom.objects.filter(teacher=is_teacher)
                # print(all_classes.values_list('id'))
                all_events = Events.objects.filter(Room__in=all_classes.values_list('id'))
                # print(all_events.values_list('id'))
                pending_video = videoUpload.objects.filter(EventID__in=all_events.values_list('id'),
                                                           Total_marks=0)
                correctVideo = videoUpload.objects.filter(EventID__in=all_events.values_list('id'),
                                                          Total_marks__gt=0)
                # print(all_video)
            else:
                return HttpResponse("Your Request Is Pending for Admin review")
        except Exception as e:
            return HttpResponse("Your Not Teacher Plz Contact your Admin")

        if request.is_ajax():

              if request.GET['videos']=="verified" :
                videos_id_list = correctVideo.values_list('id')
                User_Marks= Marks.objects.filter(videoId__in=videos_id_list)
                cur_marked=MarksSerializer(User_Marks,many=True)
                return Response({"data": cur_marked.data})
              if  request.GET['videos']=="unseen":

                #left_videos=videoUploadSerializer
                left_cur_marked =videoUploadSerializer(pending_video,many=True)
                return Response({"data":left_cur_marked.data})
        else :
            return Response ({"data":"Acess DENIED "},status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def eventsajax(request):
    if request.method == 'GET':

        try:
            is_teacher = TEACHER.objects.get(teacher=request.user)
            if is_teacher.is_active:
                all_classes = TeacherClassRoom.objects.filter(teacher=is_teacher)
                # print(all_classes.values_list('id'))
                all_events = Events.objects.filter(Room__in=all_classes.values_list('id'))
                # print(all_events.values_list('id'))
                pending_video = videoUpload.objects.filter(EventID__in=all_events.values_list('id'),
                                                           Total_marks=0)
                correctVideo = videoUpload.objects.filter(EventID__in=all_events.values_list('id'),
                                                          Total_marks__gt=0)
                # print(all_video)
            else:
                return HttpResponse("Your Request Is Pending for Admin review")
        except Exception as e:
            return HttpResponse("Your Not Teacher Plz Contact your Admin")
        if request.is_ajax():
            #allmark_user = Marks.objects.filter(moderator_email=request.user.email).order_by('EventName')
            #cur_marked=MarksSerializer(allmark_user,many=True)
            left_cur_marked =  videoUploadSerializerMark(pending_video, many=True)
            return Response({"data": left_cur_marked.data})

        else :
            return Response ({"data":"Acess DENIED "},status=status.HTTP_400_BAD_REQUEST)