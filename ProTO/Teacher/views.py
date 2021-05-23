from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from rest_framework import status

# Create your views here.

def reg_teacher(request):
    return HttpResponse ("HI")