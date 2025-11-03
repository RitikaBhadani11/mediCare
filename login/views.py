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
from patient.models import patientform
from doctor.models import doctordetail



# Create your views here.
def index(request):

    doctorTable = doctordetail.objects.all()

    params={}
    params['doctorTable']=doctorTable

    return render(request, 'authentication/home.html',params)
    # return redirect('user/')

def signup(request):
    
    # Storing details from form to User table
    if request.method=="POST":
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        password=request.POST.get("password")
        # password2=request.POST.get("confirmPass")

        # Handling Exceptions in username
        if not username.isalnum():
            messages.error(request, "Username can only contain letters and numbers.")
            return redirect('signup')
        
        # Handling UNIQUE Usernames and Emails
        elif User.objects.filter(username=username):
            messages.error(request, "Username already exist! Try another username.")
            return redirect('signup')
        
        
        elif User.objects.filter(email=email):  
            messages.error(request, "Email already exist! Try another Email.")
            return redirect('signup')
        
        


        # Handling exception in password
        # elif password1!=password2:
        #     messages.error(request,"Enter correct password for confirmation.")
        #     return redirect('signup')
        
        else:
            # Adding the details of user into User Database Table
            myuser = User.objects.create_user(username, email, password)

            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()

            messages.success(request,"Hello "+ fname +", your account has been successfully created !!!")

            user=authenticate(username=username, password=password)         
            #this will return a not none value is the user is authenticated otherwise it returns none if the user have entered the wrong credentials"""

            if user is not None:
                login(request, user)
                # messages.success(request,"Logged in !")
                return redirect("user/")
                # login(request, myuser)
            

            # ------------------------------------------------ Welcome EMAIL-----------------------------------------------
            subject = "Welcome to DocScheduler"
            message = "Hi" + myuser.username + "!! \n" + "Welcome to DocScheduler!!! \n Thank you for visiting our website. \n\n Thanking You \n DocSchedukler Team"
            from_email= settings.EMAIL_HOST_USER
            to_list= [myuser.email]

            send_mail(subject, message, from_email, to_list, fail_silently= True)
            #------------------------------------------------- Email sent -----------------------------------------------------
            
            return redirect("user/")



    return render(request, 'authentication/UserSignUp.html')

def signin(request):

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username, password=password)         
        #this will return a not none value is the user is authenticate otherwise it returns none if the user have entered the wrong credentials"""

        
        if user is not None:
            login(request, user)
            messages.success(request,"Logged in !")
            myuser=User.objects.filter(username=username)
            # fname= myuser.first_name
            return redirect("user/")
            

        else:
            messages.error(request, "Wrong Credentials")

    return render(request, 'authentication/UserLogin.html')

def signout(request):
    logout(request)
    messages.success(request, "You are successfully logged out")

    return redirect('index')


################################### Function for doctor authentication ##################################################

# Sign in function for doctors
def docsignin(request):

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username, password=password)         
        #this will return a not none value is the user is authenticate otherwise it returns none if the user have entered the wrong credentials"""

        
        if user is not None:
            login(request, user)
            drname = request.user.first_name
            messages.success(request,"Hey Dr. "+ drname + ", We heartly welcome you to our website.")
            myuser=User.objects.filter(username=username)
            # fname= myuser.first_name
            return redirect("doctor/")
            

        else:
            messages.error(request, "Wrong Credentials")


    return render(request, 'authentication/DoctorLogin.html')


# Sign up function for doctors
def docsignup(request):

     # Storing details from form to User table
    if request.method=="POST":
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        password=request.POST.get("password")
        # password2=request.POST.get("confirmPass")

        # Handling Exceptions in username
        if not username.isalnum():
            messages.error(request, "Username can only contain letters and numbers. Spaces arent allowed.")
            return redirect('docsignup')
        
        # Handling UNIQUE Usernames and Emails
        elif User.objects.filter(username=username):
            messages.error(request, "Username already exist! Try another username.")
            return redirect('docsignup')
        
        
        elif User.objects.filter(email=email):  
            messages.error(request, "Email already exist! Try another Email.")
            return redirect('docsignup')
        
        


        # Handling exception in password
        # elif password1!=password2:
        #     messages.error(request,"Enter correct password for confirmation.")
        #     return redirect('signup')
        
        else:
            # Adding the details of user into User Database Table
            myuser = User.objects.create_user(username, email, password)
        
            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()

            messages.success(request,"Hello, Dr. "+ fname +", your account has been successfully created !!!")



        
            

            # ------------------------------------------------ Welcome EMAIL-----------------------------------------------
            subject = "Welcome to DocScheduler"
            message = "Hi" + myuser.username + "!! \n" + "Welcome to DocScheduler!!! \n Thank you for visiting our website. \n\n Thanking You \n DocSchedukler Team"
            from_email= settings.EMAIL_HOST_USER
            to_list= [myuser.email]

            send_mail(subject, message, from_email, to_list, fail_silently= True)
            #------------------------------------------------- Email sent -----------------------------------------------------
            
            user=authenticate(username=username, password=password)         
            #this will return a not none value is the user is authenticated otherwise it returns none if the user have entered the wrong credentials"""

            if user is not None:
                login(request, user)
                # messages.success(request,"Logged in !")
                return redirect("doctor/")
                # login(request, myuser)
            




    return render(request, 'authentication/DoctorSignUp.html')
