from django.urls import path

from .views import *

urlpatterns = [
   path('',homepage,name="index"),
   path('upload/',upload_file,name="video"),
   path('upload/ajax', ajaxsubmitVideo.as_view(), name="upload vidoe"),

]