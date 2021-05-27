# PROTO-SEEK

# Video Sharing platform for School and college
# Tech used 
1. django (Backend)
2. django rest framework (API)
3. Ajax
4. html and css and js
5. chartjs
6. bootstrap
7. static_ranges for video
8. dj_static
9. Smpt2go for mailing verifying EMAIL ADDRESS OF USER
10. thumbnail generation useing Canvas Check out the file [link](https://github.com/engineerscodes/PROTO-SEEK/blob/91c30b3b7a21fac544e831b3ba48166b1ef7ba24/static/js/upload.js#L8)
# ITS A VIDEO ASSESSMENT  CREATE ON ORGANISATION  
 keep in mind studens,techear
# DIFFERENT LEVELS OF PRIVILEGES
<b> Students can access Few urls </b>
<b> Teacher can access Few urls </b>
<br>
<b>User have to reg to become teacher url - [link](https://protoseek.herokuapp.com/teacher/)</b>
<br>
<b> Admin of the ORGANISATION will review the request ,This method is used because Most of school or college May not have  ORGANISATION   Email </b>
<hr>
<br>

# USAGE

<br>

   1. Fork or clone to Repo 
   2. Change it As per Your ORGANISATION 
   3.<b>ADD YOUR SMPT2GO USERNAME AND PASSWORD -[CLICK](https://github.com/engineerscodes/PROTO-SEEK/blob/master/ProTO/CREAD.py) </b> 
   4. The Existing username and Password will be Changed soon
   5. CREATE YOUR SQLDB
   6. Add your email here [here](https://github.com/engineerscodes/PROTO-SEEK/blob/9fa49765680980a7ea228ad5f5135b96b9229748/Account/views.py#L39) 
   7. The mail will use this Email Address
   8. Buy your Domain name And Add it in allowed [here](https://github.com/engineerscodes/PROTO-SEEK/blob/9fa49765680980a7ea228ad5f5135b96b9229748/ProTO/settings.py#L28)
   9. Host your Django Project ON AWS OR DIGITAL OCEAN
   10. Donot Host on Heruko(Free) because Request TimeOut
   ![image](https://user-images.githubusercontent.com/68312849/119846761-0ba6a600-bf28-11eb-817f-74bbf31ed7d6.png)
   11. I have Still Hosted on Heruko (free) for now demo purpose 
   12. You cannot upload file to it ,because of Request TimeOut
   13. I recommend AWS HOSTING 
   # link -https://protoseek.herokuapp.com/teacher/
   
   # Working
   1. clone to Project Locally [](https://github.com/engineerscodes/PROTO-SEEK.git)
   2. TO Run Project
```python
 cd ProTO
 python manage.py runserver
```
   3. MakeMigration 
```python
 python manage.py makemigrations
``` 
   4. Migrate DB
```python
 python manage.py  migrate
``` 
  5. IF your making Changes in CSS OR JS (static files) and DEBUG IS FASLE then Run this Command
```python
 python manage.py  collectstatic
``` 
 6. Also you can change Static root and Media root -[STATIC URL ROOT](https://github.com/engineerscodes/PROTO-SEEK/blob/9fa49765680980a7ea228ad5f5135b96b9229748/ProTO/settings.py#L132) [MEDIA ROOT](https://github.com/engineerscodes/PROTO-SEEK/blob/9fa49765680980a7ea228ad5f5135b96b9229748/ProTO/settings.py#L155)
 
 # DB INFO
 
   1. ACCOUNTS -DJAGNO  User MODEL 
   2.  TEACHER APP
   3.  TEACHERS TABLE primaryKey is Teacher 
 ```python
 class TEACHER(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return "EMAIL: " + self.teacher.email + " | USERNAME: " + self.teacher.username
 ```
   4. TEACHERS CLASS ROOM USES OF F.K (ForeignKey) check out django doc ,PrimaryKey is ID eg(1,2,3,4,......100....)AutoField
 ```python
 class TeacherClassRoom(models.Model):
    class Meta:
        unique_together = (('teacher', 'classRoomName'))
    teacher=models.ForeignKey(TEACHER,on_delete=models.CASCADE)
    classRoomName=models.CharField(max_length=25)
    class_url=models.CharField(max_length=2000,blank=True)

    def __str__(self):
        return  str(self.id)
 ```
   5. Students in Class Table ,P.K IS ID for this Table 
 ```python
 class StudentInClassRoom(models.Model):
    class Meta:
        unique_together = (('classId', 'student'))
    classId=models.ForeignKey(TeacherClassRoom,on_delete=models.CASCADE,to_field='id')
    student=models.ForeignKey(User,on_delete=models.CASCADE)
 ```
  6. EVENT (ASSIGNMENT) PK IS ID FOR IS TABLE TOO
 ```python
class Event(models.Model):
    class Meta:
        unique_together = (('eventname', 'Room'))
    eventname = models.CharField(max_length=50)
    Room=models.ForeignKey(TeacherClassRoom,on_delete=models.CASCADE)

    def __str__(self):
        return "Room :"+self.Room.classRoomName+"| Event :"+self.eventname
 ```
  7. Till Now all the above table to linked togther with ForeignKey
  8. Video App
  9. videoUpload table PK is id for this table
  ```python
  class videoUpload(models.Model):

    captions=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    date=models.DateField(default='2001-04-12')
    EventName=models.CharField(max_length=50,default="")
    thumbnail=models.TextField()
    video=models.FileField(upload_to="videos/%y",validators=[file_size,FileExtensionValidator(allowed_extensions=['mp4','MOV','MKV'])])
    url_64encoding=models.CharField(max_length=2048,default='/upload/videos/')
    Total_marks=models.IntegerField(default=0)
    EventID=models.CharField(max_length=100,default='welcome newbie')
    def __str__(self):
        return  self.captions
    def total_marks(self):
        return self.Total_marks
  ```
  10. MarkUpload table  PK is id for this table
  ```python
  class Marks(models.Model):
    class Meta:
        unique_together=(('videoId','moderator_email'))
    videoId=models.CharField(max_length=250)
    by_email=models.CharField(max_length=250)
    marks=models.IntegerField(validators=[MinValueValidator(0)])
    moderator_email=models.CharField(max_length=250)
    video_link=models.CharField(max_length=100000)
    date=models.DateField(default='2001-04-12')
    EventName = models.CharField(max_length=50, default="")
    verfiyed=models.BooleanField(default=False)
    def __str__(self):
        return "VideoID:" +self.video_link+" BY :"+self.moderator_email
  
  ```
  
  11. Since we are usign AIP you must have serializers class for this app
  12. READ DJANGO DOC
  ```python
from rest_framework import serializers
from .models import videoUpload,Marks
from django.apps import apps
Events=apps.get_model('Event','Event')

class MarksSerializer(serializers.ModelSerializer) :
    class Meta:
        model=Marks
        #fields="__all__"
        fields=('video_link','date','by_email','EventName','marks')

class videoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model= videoUpload
        #fields="__all__"
        fields=('url_64encoding','date','username',)

class videoUploadSerializerMark(serializers.ModelSerializer):
    class Meta:
        model= videoUpload
        #fields="__all__"
        fields=('url_64encoding','date','username','EventName')

class SubmitVideo(serializers.ModelSerializer) :

    class Meta :
        model=videoUpload
        fields=('thumbnail','video','captions')
        #extra_kwargs = {'username': {'required': False}}

class VDContent(serializers.ModelSerializer):

    class Meta:
        model= videoUpload
        fields=('url_64encoding','thumbnail','captions','username','date','EventName')

class EventSerial(serializers.ModelSerializer):

    class Meta:
        model=Events
        fields='__all__'
  ```
 
   # IMAGES and HOW TO USE
   
   1. LOGIN -[LINK](https://protoseek.herokuapp.com/account/login)
   2. Activation mail
    ![image](https://user-images.githubusercontent.com/68312849/119853344-bd94a100-bf2d-11eb-90c1-f1b8501bbf5a.png)
   2.1. ADMIN MUST CHECK THIS FILED THEN ONLY The TEACHER IS VALIDATED or VERIFIED
   ![image](https://user-images.githubusercontent.com/68312849/119854796-013bda80-bf2f-11eb-8912-b984ff835bc9.png)

   3.TEACHER REG PAGE - [link](https://protoseek.herokuapp.com/teacher/) for you the message may be diffrent (like under admin review )
   ![image](https://user-images.githubusercontent.com/68312849/119853884-35fb6200-bf2e-11eb-9701-e5d94de95d50.png)

   4 . CREATE CLASS AND SHARE THE CODE WITH STUDENTS  [link](https://protoseek.herokuapp.com/teacher/newclassroom/)
     ![image](https://user-images.githubusercontent.com/68312849/119855034-35170000-bf2f-11eb-9b42-f55033447044.png)
     
   5 . Only Teacher can see this Page HOMEPAGE FOR teacher
   ![image](https://user-images.githubusercontent.com/68312849/119855255-61cb1780-bf2f-11eb-8dc0-c123616cec76.png)
   ![image](https://user-images.githubusercontent.com/68312849/119855328-6e4f7000-bf2f-11eb-9923-d99641fb557f.png)
   
   6. ON click  any class you will get all students list ,event and create a event for the class -(event means assignments)
   ![image](https://user-images.githubusercontent.com/68312849/119857128-eec2a080-bf30-11eb-9666-9c23a621b6a4.png)
   ![image](https://user-images.githubusercontent.com/68312849/119857228-0568f780-bf31-11eb-866f-74c0c031f23a.png)

   
   
   7. assign marks to video
   ![image](https://user-images.githubusercontent.com/68312849/119856924-bb801180-bf30-11eb-9e16-68f2ed02ef94.png)

   
   8. Click on video will open The vidoe for You in above image
   9. Teacher can get all stat ,about uploads and pending videos  (link)[https://protoseek.herokuapp.com/teacher/info/]
   ![image](https://user-images.githubusercontent.com/68312849/119855567-a5258600-bf2f-11eb-8bc6-1300d01108cf.png)
    ![image](https://user-images.githubusercontent.com/68312849/119855629-b53d6580-bf2f-11eb-8840-5d979d09ab3c.png)
   10. for Students the HomePage is [link](https://protoseek.herokuapp.com/student/)
   ![image](https://user-images.githubusercontent.com/68312849/119856097-16fdcf80-bf30-11eb-9ece-d7f5e6969a2f.png)
   11. upload page [link](https://protoseek.herokuapp.com/upload/)
   ![image](https://user-images.githubusercontent.com/68312849/119856328-4280ba00-bf30-11eb-8014-77cbad588395.png)
   12. Import Join class [link](https://protoseek.herokuapp.com/teacher/join/)
   ![image](https://user-images.githubusercontent.com/68312849/119857413-29c4d400-bf31-11eb-9649-93414951708d.png)

   
  
  


 

 
  

