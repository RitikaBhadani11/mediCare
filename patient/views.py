#importing required modules
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User                         #importing User model for authentication
from django.contrib import messages                                 #importing messages to display message when user signups
from django.contrib.auth import authenticate, login, logout
from hackathonProject import settings
from django.core.mail import send_mail 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage,send_mail
from doctor.models import doctordetail, slot_table
from patient.models import patientform, booking, datewise_slot
from django.db.models import Q
from datetime import date



# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("index")


    # patient_detail = patientform()
    # if not patientform.objects.filter(fname=request.user.first_name) :
    #     patient_detail=patientform(pusername=request.user.username, fname=request.user.first_name, lname=request.user.last_name, pemail=request.user.email)

    #     patient_detail.save()

        

    doctorTable = doctordetail.objects.all()

    params={}
    params['doctorTable']=doctorTable

    
        

    return render(request, 'patient/home.html',params)



    

def doctorinfo_slot(request):
    if not request.user.is_authenticated:
        return redirect("index")
    
    current_booking = booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

    # Details of the doctor selected by patient
    selected_doctor = doctordetail.objects.filter(dusername = current_booking.doctor)[0]

    ####---------------------------------- Slot calculation----------------------------------#####
    
    # # Extracting time in string
    # fromhrs, frommin = selected_doctor.fromtime.split(':')
    # tohrs, tomin = selected_doctor.totime.split(':')

    # # Converting time to int
    # # fromhrs = int(fromhrs)
    # # frommin = int(frommin)
    # # tohrs = int(tohrs)
    # # tomin = int(tomin)

    # # Storing avg time in int format
    # avgtime = int(selected_doctor.avgtime)
    
    # totalmins= (abs(int(fromhrs)- int(tohrs))*60 )+ abs(int(frommin)-int(tomin))
    # Totalslots = totalmins//avgtime

    # slot=[str(fromhrs)+':'+str(frommin)]

    # for i in range(1,Totalslots+1):
    #     fromhrs, frommin=slot[i-1].split(':')
    #     if int(frommin)+avgtime < 60:

    #         addedmins = int(frommin)+avgtime
    #         createdSlot =(fromhrs +':'+str(addedmins))
    #         slot.append(createdSlot)
        
    #     elif int(frommin)+avgtime ==  60:
    #         addedhrs = (int(fromhrs)+1)
    #         createdSlot = str(addedhrs)+':'+'00'
    #         slot.append(createdSlot)


    #     else:
    #         remaining_mins = 60 - (int(frommin)+avgtime)
    #         addedhrs = (int(fromhrs)+1)
    #         createdSlot = str(addedhrs)+':'+ str(remaining_mins)
    #         slot.append(createdSlot)

    # print(slot)

    # SLOT = {}
    # slot_countList = []
    # start = 0
    # hour = (slot[0][0:2])    
    # hour = int(hour)
    # total_hrs = 0
    # for j in range(len(slot)):
    #     if int(slot[j][0:2]) == hour + 1:
    #         slotcount = abs(start - (j))
    #         start= j
            
    #         if len(slot[j][0:2]) == 1:
    #             time = ("0"+str(hour)+":00") +" -> "+ ("0"+str(hour+1)+":00")
    #             SLOT[time]=slotcount
    #         else:
    #             time = (str(hour)+":00") +" -> "+ (str(hour+1)+":00")
    #             SLOT[time]=slotcount


    #         hour = hour +1
    #         total_hrs = total_hrs+1
    
    # print(SLOT)



    #-----------------------------------------Slot calculation ends ------------------------------------------
    
    # selected_slot_instance = slot_table.objects.filter(doc_username = selected_doctor.dusername)[0]

    datewise_slot_instance = datewise_slot.objects.filter(doc_username = selected_doctor.dusername, date = current_booking.date)[0]


    # today = date.today()

    # for i in selected_slot_instance:
    #     if i.date == today.strftime("%d/%m/%Y"):
    #         SLOT = i.slotDict

        




# # dd/mm/YY

# today = date.today()
# d1 = today.strftime("%d/%m/%Y")
# print("d1 =", d1)

    print(datewise_slot_instance.morning_updatedSlotdict)

    params={
        'morningSLOT' : datewise_slot_instance.morning_updatedSlotdict,
        'eveningSLOT' : datewise_slot_instance.evening_updatedSlotdict,
        'username': selected_doctor.dusername,
        'fname': selected_doctor.fname,
        'lname': selected_doctor.lname,
        'email': selected_doctor.email,
        'contact': selected_doctor.contact,
        'image': selected_doctor.image,
        'specialization': selected_doctor.specialization,
        'specdegree': selected_doctor.specdegree,
        'license': selected_doctor.license,
        'shortdesc': selected_doctor.shortdesc,
        'desc': selected_doctor.desc,
        'fromtime' : selected_doctor.fromtime,
        'totime' : selected_doctor.totime,
        'eveningfromtime' : selected_doctor.eveningfromtime,
        'eveningtotime' : selected_doctor.eveningtotime,
        'avgtime': selected_doctor.avgtime,
        'housenum': selected_doctor.housenum,
        'hcity': selected_doctor.hcity,
        'hlandmark': selected_doctor.hlandmark,
        'hzip': selected_doctor.hzip,
        'hstate': selected_doctor.hstate,
        'clocation': selected_doctor.clocation,
        'ccity': selected_doctor.ccity,
        # 'clandmark': particular_doc.clandmark,
        'czip': selected_doctor.czip,
        'cstate': selected_doctor.cstate,
        }

    print(params["image"])

    return render(request, "patient/doctorinfomain_slot.html", params)



def form(request):
    if not request.user.is_authenticated:
        return redirect("index")


    particular_booking=booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

    # particular_patient=patientform.objects.filter(pusername= request.user.username)[0]

    if request.method == "POST":

        #Extracting values from form
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        age = request.POST.get("age")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        bloodgrp = request.POST.get("bloodgrp")
        gender = request.POST.get("gender")
        # email = request.POST.get("email")

        contact = request.POST.get("contact")
        
        state = request.POST.get("state")
        
        allergy = request.POST.get("allergy")
        
        medications = request.POST.get("medications")
        
        insurance = request.POST.get("insurance")
        
        drughistory = request.POST.get("drughistory")
        symptoms = request.POST.get("symptoms")
        medicalhistory = request.POST.get("medicalhistory")

        #Updating values in model
        particular_patient=patientform()

        particular_patient.dusername = particular_booking.doctor
        particular_patient.slot = particular_booking.slot
        particular_patient.slotNum = particular_booking.slotNum
        particular_patient.date = particular_booking.date
        
        particular_patient.pusername = request.user.username
        particular_patient.pemail = request.user.email
        particular_patient.fname = fname
        particular_patient.lname = lname
        particular_patient.age = age
        particular_patient.height = height
        particular_patient.weight = weight
        particular_patient.bloodgrp = bloodgrp
        particular_patient.gender = gender
        particular_patient.contact = contact
        particular_patient.state = state
        particular_patient.allergy = allergy
        particular_patient.goingonMedications = medications
        particular_patient.insurance = insurance
        particular_patient.drughistory = drughistory
        particular_patient.symptoms = symptoms
        particular_patient.medicalhistory = medicalhistory


        particular_patient.save()

        # Handling Booking table for patientDetails

        
        particular_booking.patientdetail= particular_patient

        particular_booking.save()

        datewise_slot_instance = datewise_slot.objects.filter(doc_username = particular_booking.doctor, date= particular_booking.date)[0]

        #takeing the slotDict from datewise_slot_instance
        morning_UpdatedSlotdict = datewise_slot_instance.morning_updatedSlotdict

        for i in datewise_slot_instance.morning_updatedSlotdict:
            if i==particular_booking.slot:
                morning_UpdatedSlotdict[i] = morning_UpdatedSlotdict[i]-1

        print(morning_UpdatedSlotdict)

        evening_UpdatedSlotdict = datewise_slot_instance.evening_updatedSlotdict

        for i in datewise_slot_instance.evening_updatedSlotdict:
            if i==particular_booking.slot:
                evening_UpdatedSlotdict[i] = evening_UpdatedSlotdict[i]-1

        print(evening_UpdatedSlotdict)


        datewise_slot_instance.morning_updatedSlotdict = morning_UpdatedSlotdict
        datewise_slot_instance.evening_updatedSlotdict = evening_UpdatedSlotdict
        datewise_slot_instance.save()
        
                

        return redirect("home")
    

    params={
        # "fname": particular_patient.fname,
        # "lname": particular_patient.lname,
        # "age": particular_patient.age,
        # "height": particular_patient.height,
        # "weight": particular_patient.weight,
        # "bloodgrp": particular_patient.bloodgrp,
        # "gender": particular_patient.gender,
        "email": request.user.email,

        # "contact": particular_patient.contact,
        
        # "state": particular_patient.state,
        
        # "allergy": particular_patient.allergy,
        
        # "medications": particular_patient.goingonMedications,
        
        # "insurance": particular_patient.insurance,
        
        # "drughistory": particular_patient.drughistory,
        # "symptoms": particular_patient.symptoms,
        # "medicalhistory": particular_patient.medicalhistory
        
    }

    return render(request, 'patient/form.html', params)


# --------------------------------------- Updation of booking table ---------------------------------



def updatebooking_after_docselection(request):          #Updation of booking table after choosing a doctor in home page

    if not request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        dusername = request.POST.get("doctorusername")

        bookingobject = booking()
        bookingobject.doctor= dusername
        bookingobject.bookingid= request.user.id
        bookingobject.pusername= request.user.username
        bookingobject.pfname= request.user.first_name
        bookingobject.plname= request.user.last_name

        bookingobject.save()

        # datewise_slot_instance = datewise_slot(doc_username =dusername)
        # datewise_slot_instance.save()


        return redirect("doctorinfo_date")
    


def updatebooking_after_goingbackdate(request):                 # updation after clicking back button in doctors info page

    if not request.user.is_authenticated:
        return redirect("index")

    particular_booking=booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

    particular_booking.delete()

    return redirect("home") 


def updatebooking_after_goingbackslot(request):
    if not request.user.is_authenticated:
        return redirect("index")

    particular_booking=booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

    particular_booking.date = None
    particular_booking.save()

    return redirect("doctorinfo_date")





def updatebooking_after_logout(request):                 # updation after clicking back button in doctors info page

    if not request.user.is_authenticated:
        return redirect("index")


    particular_booking=booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

    # if datewise_slot.objects.filter(doc_username = particular_booking.doctor, date=particular_booking.date)[0]:
    #     datewise_slot_instance = datewise_slot.objects.filter(doc_username = particular_booking.doctor, date=particular_booking.date)[0]
    #     datewise_slot_instance.delete():


    particular_booking.delete()


    return redirect("signout")

def updatebooking_after_slotselection(request):

    if not request.user.is_authenticated:
        return redirect("index")

    particular_booking=booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

    if request.method == "POST":
        # selected_date = request.POST.get("date")
        slotTime = request.POST.get("slotTime")
        slotNum = request.POST.get("slotNum")

        particular_booking.slot= slotTime
        
        particular_booking.slotNum= slotNum

        # particular_booking.= request.user.id

        particular_booking.save()


        return redirect("form")


def updatebooking_after_goingbackform(request):
    if not request.user.is_authenticated:
        return redirect("index")
    
    particular_booking=booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

    particular_booking.slot= None
    particular_booking.slotNum= None

    return redirect("doctorinfo_slot")

def doctorinfo_date(request):

    if not request.user.is_authenticated:
        return redirect("index")
        

    particular_booking=booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()
    
    current_booking = booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

    selected_doctor = doctordetail.objects.filter(dusername = current_booking.doctor)[0]

    params={
        # 'SLOT' : datewise_slot_instance.updatedSlotdict,
        'username': selected_doctor.dusername,
        'fname': selected_doctor.fname,
        'lname': selected_doctor.lname,
        'email': selected_doctor.email,
        'contact': selected_doctor.contact,
        'image': selected_doctor.image,
        'specialization': selected_doctor.specialization,
        'specdegree': selected_doctor.specdegree,
        'license': selected_doctor.license,
        'shortdesc': selected_doctor.shortdesc,
        'desc': selected_doctor.desc,
        'fromtime' : selected_doctor.fromtime,
        'totime' : selected_doctor.totime,
        'eveningfromtime' : selected_doctor.eveningfromtime,
        'eveningtotime' : selected_doctor.eveningtotime,
        'avgtime': selected_doctor.avgtime,
        'housenum': selected_doctor.housenum,
        'hcity': selected_doctor.hcity,
        'hlandmark': selected_doctor.hlandmark,
        'hzip': selected_doctor.hzip,
        'hstate': selected_doctor.hstate,
        'clocation': selected_doctor.clocation,
        'ccity': selected_doctor.ccity,
        # 'clandmark': particular_doc.clandmark,
        'czip': selected_doctor.czip,
        'cstate': selected_doctor.cstate,
        }

    # Details of the doctor selected by patient
    

    if request.method == "POST":
        
        selected_date = request.POST.get("date")

        particular_booking.date= selected_date
        particular_booking.save()
        

        particular_booking=booking.objects.filter(Q(pusername= request.user.username) & Q(pfname= request.user.first_name) & Q(bookingid= request.user.id)).last()

        if (datewise_slot.objects.filter(date = selected_date, doc_username = particular_booking.doctor)): 
           return redirect("doctorinfo_slot")
        
        slot_table_instance = slot_table.objects.filter(doc_username = particular_booking.doctor)[0]
        # print(slot_table_instance.slotDict)

        datewise_slot_instance = datewise_slot(date = selected_date, morning_updatedSlotdict= slot_table_instance.morningslotDict, evening_updatedSlotdict= slot_table_instance.eveningslotDict, doc_username = particular_booking.doctor) 
        datewise_slot_instance.save()


        

        return redirect("doctorinfo_slot")
    
    return render(request, "patient/doctorinfomain_date.html", params)
                




