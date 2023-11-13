from django.db import models
from django.contrib.auth.hashers import make_password
# User Registration Section

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
    
    def str(self):
        return self.nickname
    
    def get_email_field_name(self):
        return 'email'


