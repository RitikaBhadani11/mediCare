from django.db import models
from django.contrib.auth.models import User

# Create your models here
class doctordetail(models.Model):

    #Doctor's general details
    # duser = models.ForeignKey(User, on_delete=models.CASCADE)
    dusername = models.CharField(max_length=255)
    fname = models.CharField(max_length=50, null=True)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    contact = models.BigIntegerField(default=0)
    image = models.ImageField(upload_to="doctor/images", default='')
    specialization = models.CharField(max_length=100, default='', null=True)
    specdegree = models.FileField(upload_to="doctor/files", default='')
    license = models.FileField(upload_to="doctor/files", default='')

    #Description of doctor in detail
    shortdesc = models.CharField(max_length=500,default='', null=True)
    desc = models.CharField(max_length=500,default='', null=True)

    # When doctor is available
    fromtime = models.CharField(max_length=5, default='', null=True)
    totime = models.CharField(max_length=5, default= '', null=True)

    eveningfromtime = models.CharField(max_length=5, default='', null=True)
    eveningtotime = models.CharField(max_length=5, default= '', null=True)


    #avg amount of time required to see a patient
    avgtime= models.CharField(max_length=20,default= '', null=True)

    # Doctor's Home address details
    housenum= models.CharField(max_length= 75,default= '', null=True)
    hcity = models.CharField(max_length=20,default= '', null=True)
    hlandmark = models.CharField(max_length=50,default= '', null=True)
    hzip = models.IntegerField(default=0, null=True)
    hstate = models.CharField(max_length=50,default= '', null=True)

    #Doctor's clinic/hospital address details
    clocation= models.CharField(max_length= 75,default= '', null=True)
    ccity = models.CharField(max_length=20,default= '', null=True)
    # clandmark = models.CharField(max_length=50,default= None)
    czip = models.IntegerField(default=0, null=True)
    cstate = models.CharField(max_length=50,default= '', null=True)

    # name = 'Dr. '+ fname + ' '+ lname


    def __str__(self):
        
        return self.fname
    


# Model for handling slot data of each doctor    
class slot_table(models.Model):
    doc_username = models.CharField(max_length=50, null = True)
    morningslotDict = models.JSONField(null=True, default = None)
    eveningslotDict = models.JSONField(null=True, default = None)
    date = models.DateField(null=True)
