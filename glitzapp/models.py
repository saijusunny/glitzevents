from django.db import models
from django.contrib.auth.hashers import make_password
# User Registration Section
from datetime import datetime,date, timedelta
from  embed_video.fields  import  EmbedVideoField  #pip install django django-embed-video
role = (
    ("user1", "Staff"),
    ("user2", "User"),
   
)

class User_Registration(models.Model):
    
    name = models.CharField(max_length=255,blank=True,null=True)
    phone_number = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    role = models.CharField(max_length=255,blank=True,null=True,choices = role)
    pro_pic = models.ImageField(upload_to='images/propic', default='static/images/logo/icon.png')
    username = models.CharField(max_length=255,blank=True,null=True)
    password = models.CharField(max_length=255,blank=True,null=True)
    status =models.CharField(max_length = 255,blank=True,null=True, default="active")
    addres =  models.TextField(blank=True,null=True)
    joindate = models.DateField(null=True)
    last_login = models.DateTimeField(null=True, blank=True)    
    def str(self):
        return self.nickname
    
    def get_email_field_name(self):
        return 'email'

class events_table(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    event_title = models.CharField(max_length=255, blank=False, null=False)
    posting_date = models.DateField(default=date.today())
    cover_image = models.ImageField(upload_to='images/cover', default='static/images/logo/icon.png')
    description=models.TextField(blank=True, null=True)

class event_empeded_link(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    events = models.ForeignKey(events_table, on_delete=models.SET_NULL, null=True, blank=True)
    empeded_link = EmbedVideoField()


class event_images(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    events = models.ForeignKey(events_table, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='images/album', default='static/images/logo/icon.png')

class event_social(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    events = models.ForeignKey(events_table, on_delete=models.SET_NULL, null=True, blank=True)
    social_media = models.CharField(max_length=255, blank=False, null=False)
    link = models.TextField(blank=True, null=True)