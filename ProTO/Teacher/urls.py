from django.urls import path

from .views import *

urlpatterns = [
   path('',reg_teacher,name="teacher_signup"),

]