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
           
                
        if User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user1", status="active").exists():
            member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
            request.session['userid'] = member.id
            return redirect('home')
        

        elif user.is_superuser:
                request.session['userid'] = request.user.id
                return redirect('admin_home')
        else:
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
def user_registrations(request):
    if request.method=="POST":
        
        emails=request.POST.get('email',None)
        usernames=request.POST.get('username',None)
        passwords=request.POST.get('password',None)
        cn_passs=request.POST.get('cn_pass',None)
       

        if passwords == cn_passs:
            if User_Registration.objects.filter(username=usernames).exists():
                messages.error(request,'Username already registered')
                return render (request, 'user/user_signup.html')
            else:
                if User_Registration.objects.filter(email=emails).exists():
                    messages.error(request,'Email already registered')
                    return render (request, 'user/user_signup.html')
                else:
                    usrs=User_Registration()
                    usrs.name = request.POST.get('fullname',None)
                    usrs.phone_number = request.POST.get('phno',None)
                    usrs.email = request.POST.get('email',None)
                    usrs.role ="user1"
                    if request.FILES.get('prop',None)==None:
                        usrs.pro_pic='static\images\logo\icon.png'
                    else:
                        usrs.pro_pic =request.FILES.get('prop',None)
                    
                    usrs.username = request.POST.get('username',None)
                    usrs.password = request.POST.get('password',None)
                    usrs.status = "active"
                    usrs.addres =request.POST.get('address',None)
                    usrs.joindate = date.today()
                    usrs.save()
                    return redirect('login_main')
        messages.error(request,"Password And Confirm Password are Not same")
        return render (request, 'user/user_signup.html')

    return render(request, "user/user_signup.html")


def base_sub(request):
    ids=request.session['userid']
    usr=User_Registration.objects.get(user=ids)
    
 
    context={
        'user':usr,
    }
    return render(request, 'user/base_sub.html',context)


def home(request):
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    context={
        'user':usr,
    }
    return render(request, 'user/home.html',context)



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


def all_events_view(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')

    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    context={
        'user':usr,
    }
    return render(request,'user/all_events.view.html',context)

def create_event(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')

    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    context={
        'user':usr,
    }

    if request.method == "POST":
        evn=events_table()
        evn.user=usr
        evn.event_title=request.POST.get('title', None)
        evn.cover_image=request.FILES.get('cover_photo', None)
        evn.description=request.POST.get('description', None)
        evn.save()

        #empeded link

        empeded = request.POST.getlist('empeded_link[]')
        if empeded:
            mappeds = zip(empeded)
            mappeds=list(mappeds)
            for ele in mappeds:
            
                created = event_empeded_link.objects.get_or_create(empeded_link=ele[0], user=usr, events=evn)
        else: 
            pass

        #images

        img = request.FILES.getlist('images[]')
        if img:
            mappeds2 = zip(img)
            mappeds2=list(mappeds2)
            for ele in mappeds2:
            
                created = event_empeded_link.objects.get_or_create(image=ele[0], user=usr, events=evn)
        else: 
            pass

        #Social Media

        md = request.POST.getlist('media[]')
        links = request.POST.getlist('link[]')
        if len(md)==len(links):
            mappeds2 = zip(md,links)
            mappeds2=list(mappeds2)
            for ele in mappeds2:
            
                created = event_empeded_link.objects.get_or_create(social_media=ele[0],link=ele[1], user=usr, events=evn)
        else: 
            pass
        return redirect('all_events_view')

    return render (request, 'user/create_event.html',context)