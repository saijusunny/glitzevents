from django.urls import re_path,path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #############################################################<<<<<<<<< LANDING MODULE >>>>>>>>>>>>>>>>>
    path('', views.index, name='index'),
    path('login_main',views.login_main, name='login_main'),
    path('forgotPassword/', views.forgotPassword,name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate,name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword,name='resetPassword'),
    path('logout/', views.logout,name='logout'),
    
    ############################################################ <<<<<<<<< User MODULE >>>>>>>>>>>>>>>>>

    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_user_profile/<int:id>',views.edit_user_profile,name='edit_user_profile'), 
    ]