from django.contrib import admin
from django.urls import path, include
from . import views                                            # Importing views.py 

urlpatterns = [
    path('', views.home, name="home"),   
    path('form', views.form, name="form"),   
    path('doctorinfo_date', views.doctorinfo_date, name="doctorinfo_date"),   
    path('doctorinfo_slot', views.doctorinfo_slot, name="doctorinfo_slot"),   
    path('updatebookingads', views.updatebooking_after_docselection, name="updatebooking_after_docselection"),   
    path('updatebookingbackslot', views.updatebooking_after_goingbackslot, name="updatebooking_after_goingbackslot"),   
    path('updatebookingbackdate', views.updatebooking_after_goingbackdate, name="updatebooking_after_goingbackdate"),   
    path('updatebookinglogout', views.updatebooking_after_logout, name="updatebooking_after_logout"),   
    path('updatebookingslot', views.updatebooking_after_slotselection, name="updatebooking_after_slotselection"),   
    path('updatebookingformback', views.updatebooking_after_goingbackform, name="updatebooking_after_goingbackform"),   

]     