from django.contrib import admin
from django.urls import path, include
from . import views                                            # Importing views.py 


# creating routes
urlpatterns = [
    path('', views.index, name="index"),        
    path('signup', views.signup, name="signup")  ,      
    path('signin', views.signin, name="signin")  ,      
    path('signout', views.signout, name="signout")  ,           
    path('docsignup', views.docsignup, name="docsignup")  ,           
    path('docsignin', views.docsignin, name="docsignin")  ,           
               
]

