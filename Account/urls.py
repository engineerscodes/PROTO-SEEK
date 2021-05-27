from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
   path('reg/',views.reg,name="reg"),
   path('login/',views.login_view,name="login"),
   path('logout/',views.logout,name="LOGOUT"),
   path('activate/<uidb64>/<token>',views.AUTHUSERNAME,name="activate")
]
