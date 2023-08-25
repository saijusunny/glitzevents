from django.shortcuts import render

# Create your views here.from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash

import random
import string
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime,date, timedelta
from django.db.models import Q
from django.template.loader import get_template

######################################################################### <<<<<<<<<< LANDING MODULE >>>>>>>>>>>>>>

def index(request):
    
    return render(request, 'index/index.html')


def login_main(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password = request.POST['password']
        print(username)
        user = authenticate(username=username, password=password)
        
        try:
            if User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user1").exists():

                member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
                
                request.session['userid'] = member.id
                if Profile_User.objects.filter(user_id=member.id).exists():
                    return redirect('staff_home')
                else:
                    return redirect('profile_staff_creation')
                
                
            elif User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user2", status="active").exists():
                member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
                request.session['userid'] = member.id
                if Profile_User.objects.filter(user_id=member.id).exists():
                    return redirect('home')
                else:
                    return redirect('profile_user_creation')

            elif user.is_superuser:
                    request.session['userid'] = request.user.id
                    return redirect('admin_home')
            else:
                messages.error(request, 'Invalid username or password')
        except:
            messages.error(request, 'Invalid username or password')
    return render(request,'index/login.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if  User_Registration.objects.filter(email=email).exists():
            user =  User_Registration.objects.get(email=email)

        

            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('index/forget-password/reset_password_email.html',{
                'user':user,
                'domain' :current_site,
                'user_id' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            }) 

            to_email = email
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()

            messages.success(request,"Password reset email has been sent your email address.")
            return redirect('login_main')
        else:
            messages.error(request,"This account does not exists !")
            return redirect('forgotPassword')
    return render(request,'index/forget-password/forgotPassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user =  User_Registration._default_manager.get(pk=user_id)  
    except(TypeError,ValueError,OverflowError, User_Registration.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['user_id'] = user_id 
        messages.success(request,"Please reset your password.")
        return redirect('resetPassword')
    else:
        messages.error(request,"The link has been expired !")
        return redirect('login_main')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('user_id') 
            user =  User_Registration.objects.get(pk=uid)
            user.password = password
            user.save()
            messages.success(request,"Password reset successfull.")
            return redirect('login_main')

        else:
            messages.error(request,"Password do not match")
            return redirect('resetPassword')
    else:
        return render(request,'index/forget-password/resetPassword.html')

def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')


########################################################## <<<<<<<<<< USER MODULE >>>>>>>>>>>>>>>>

def base_sub(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    lk=category.objects.get(id=1)
    crt_cnt=cart.objects.filter(user=ids).count()
 
    context={
        'user':usr,
        "lk":lk,
        "crt_cnt":2
    }
    return render(request, 'user/base_sub.html',context)

def user_base(request):
    ids=request.session['userid']
    usr=Profile_User.objects.get(user=ids)
    lk=category.objects.get(id=1)
    crt_cnt=cart.objects.filter(user=ids).count()
 
    context={
        'user':usr,
        "lk":lk,
        "crt_cnt":crt_cnt
    }
    return render(request, 'user/user_base.html',context)

   

  
def user_profile(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    

    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    pro=Profile_User.objects.get(user=ids)
    crt_cnt=cart.objects.filter(user=ids).count()
    return render(request, 'user/user_profile.html',{'usr':usr,'pro':pro, 'user':pro,"crt_cnt":crt_cnt})

def edit_user_profile(request,id):

    if request.method == "POST":
        form = User_Registration.objects.get(id=id)
        eml=form.email
        usr_nm=form.username
        form.name = request.POST.get('name',None)
        form.lastname = request.POST.get('lastname',None)
        form.nickname = request.POST.get('nickname',None)
        form.gender = request.POST.get('gender',None)
        form.date_of_birth = request.POST.get('date_of_birth',None)
        form.phone_number = request.POST.get('phone_number',None)
        form.email = request.POST.get('email',None)
       
        form.username = request.POST.get('username',None)
        if request.POST.get('password',None) == "":
            form.password == form.password
        else:
            if request.POST.get('password',None) == request.POST.get('con_password',None):
                form.password == request.POST.get('password',None)
            else:
                messages.error(request,"Passwords do not match!")
                return redirect ("user_profile")
       
        if str(request.POST.get('email',None)) == str(eml):
            if str(request.POST.get('username',None)) == str(usr_nm):
                form.save()
            else:
                if User_Registration.objects.filter(username=form.username).exists():
                    messages.error(request,"Username already exists.")
                    return redirect ("user_profile")
                else:
                        form.save()
        else: 
           
            if User_Registration.objects.filter(email=form.email).exists():
                messages.error(request,"Email already exists.")
                return redirect ("user_profile")
            else:
                if str(request.POST.get('username',None)) == str(usr_nm):
                    form.save()
                else:
                    if User_Registration.objects.filter(username=form.username).exists():
                        messages.error(request,"Username already exists.")
                        return redirect ("user_profile")
                    else:
                        form.save()
   
        
        return redirect ("user_profile")
    return redirect ("user_profile")
