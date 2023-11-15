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
    path('user_registrations/', views.user_registrations,name='user_registrations'),
    
    ############################################################ <<<<<<<<< User MODULE >>>>>>>>>>>>>>>>>
    path('home',views.home,name='home'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_user_profile/<int:id>',views.edit_user_profile,name='edit_user_profile'),
    path('all_events_view',views.all_events_view,name="all_events_view"),
    path('create_event',views.create_event,name="create_event"),
    path('view_all_event/<int:id>',views.view_all_event,name="view_all_event"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('view_self_event/<int:id>',views.view_self_event,name="view_self_event"),
    path('edit_event/<int:id>',views.edit_event,name="edit_event"),
    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_user_profile/<int:id>',views.edit_user_profile,name='edit_user_profile'),
    path('send_emails/',views.send_emails,name='send_emails'),
    path('send_email_index/',views.send_email_index,name='send_email_index'),

    

    ]