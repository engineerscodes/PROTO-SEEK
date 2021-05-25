from django.shortcuts import render,redirect
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
from .serializers import  videoUploadSerializer,MarksSerializer,SubmitVideo,VDContent,EventSerial
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from datetime import date
from django.utils.encoding import force_text, force_bytes
Events=apps.get_model('Event','Event')

def homepage(request):
    return HttpResponse(request.user.username)


def upload_file(request):

    if request.method =="GET":
        user = request.user
        if (user.is_authenticated == False):
            return redirect('/account/login')

        form = vd_form()
        event=Events.objects.all()
        #event=Events.objects.filter(student=request.user)

        return render(request, "upload.html", {"form": form,"event":event})
    else :
        return redirect('/account/login')



class  ajaxsubmitVideo(APIView):
 parser_classes = [MultiPartParser, FormParser,FileUploadParser]

 def post(self, request, format=None):

   user = request.user
   if (user.is_authenticated):
       serializerss = SubmitVideo(data=request.data)
       #print(request.POST.get('captions'))

       if serializerss.is_valid():
           #print(serializerss.validated_data[''])
           #print(request.POST['events'])
           form = vd_form(data=request.POST, files=request.FILES)
           if form.is_valid():
               new_form = form.save(commit=False)
               new_form.username =request.user.email
               new_form.date = date.today().strftime('%Y-%m-%d')
               new_form.save()
               video = videoUpload.objects.get(pk=new_form.id)
               video.url_64encoding = urlsafe_base64_encode(force_bytes(new_form.id))
               video.thumbnail = serializerss.validated_data['thumbnail']
               video.EventName=request.POST['events']
               video.save()
               #serializerss.save(username=request.user.email,date= date.today().strftime('%Y-%m-%d'))
               #print(videoUpload.objects.filter(pk=serializerss))
           return Response("VIDEO SUMBITTED", status=status.HTTP_200_OK)
       else:
           return Response(serializerss.errors, status=status.HTTP_400_BAD_REQUEST)
   else :
       return Response(data="access denied",status=status.HTTP_400_BAD_REQUEST)
