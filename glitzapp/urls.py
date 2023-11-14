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
    

    ]