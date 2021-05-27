from django.urls import path

from .views import *

urlpatterns = [
   path('',homepage,name="index"),
   path('upload/',upload_file,name="video"),
   path('upload/ajax', ajaxsubmitVideo.as_view(), name="upload_vidoe"),
   path('videos/',allVideos_of_class,name="gallery"),
   path('videos/<uuid>',getSingleVideo,name="Filter_Video"),
   path('student/',Home_student,name="Student_Page"),
   path('student/class/<str:cl_name>/<str:cl_id>',get_class,name="Class"),
   path('getcontent/', getcontent, name="HOME_PAGE_VIDEO"),
   path('teacher/info/',classesInof,name="class_details"),
   path('analaytics/', analaytics, name="Analaytics"),
   path('moderator/ajax',ajaxModeration,name="GETMODEAJAX"),
   path('events/', eventsajax, name="sort by events"),
]