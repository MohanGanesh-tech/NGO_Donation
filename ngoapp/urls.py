# from django.conf.urls import url, include
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 
 
urlpatterns = [

    #======================================= User =========================================
    path('',views.userloginpage,name='userloginpage'),
    path('userlogin',views.userlogin,name='userlogin'),

    path('usersignuppage',views.usersignuppage,name='usersignuppage'),
    path('usersignup',views.usersignup,name='usersignup'),

    path('userlogout',views.userlogout,name='userlogout'),

    path('userhome',views.userhome,name='userhome'),

    path('userdonatepage',views.userdonatepage,name='userdonatepage'),
    path('userdonate',views.userdonate,name='userdonate'),
    
    path('userpendingpage',views.userpendingpage,name='userpendingpage'),
    path('userapporvedpage',views.userapporvedpage,name='userapporvedpage'),
    path('userrejectedpage',views.userrejectedpage,name='userrejectedpage'),
    

    #======================================= Admin =========================================
            
    path('admin',views.adminloginpage,name='adminloginpage'),
    path('adminlogin',views.adminlogin,name='adminlogin'),

    path('adminlogout',views.adminlogout,name='adminlogout'),

    path('adminhomepage',views.adminhomepage,name='adminhomepage'),

    path('adminpendingpage',views.adminpendingpage,name='adminpendingpage'),

    path('adminapporvedpage',views.adminapporvedpage,name='adminapporvedpage'),
    path('adminapporve/<int:uid>/<int:sid>',views.adminapporve,name='adminapporve'),

    path('adminrejectedpage',views.adminrejectedpage,name='adminrejectedpage'),
    path('adminreject/<int:uid>/<int:sid>',views.adminreject,name='adminreject'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
