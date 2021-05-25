from django.urls import path

from .views import *

urlpatterns = [
   path('',homepage,name="index"),
   path('upload/',upload_file,name="video"),
   path('upload/ajax', ajaxsubmitVideo.as_view(), name="upload vidoe"),
   #path('videos/',allVideos,name="gallery"),
   path('videos/<uuid>',getSingleVideo,name="Filter Video"),
   path('student/',Home_student,name="Student Page"),
   path('student/class/<str:cl_name>/<str:cl_id>',get_class,name="Class"),
]