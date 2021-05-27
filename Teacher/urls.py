from django.urls import path

from .views import *

urlpatterns = [
   path('',reg_teacher,name="teacher_signup"),
   path('newclassroom/',new_class,name="new class"),
   path('join/',join_class,name="join room"),
   path('class/<str:cl_id>',view_class,name="class list"),


]