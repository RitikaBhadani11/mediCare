from django.contrib import admin
from .models import patientform, booking, datewise_slot

# Register your models here.
admin.site.register(patientform)
admin.site.register(booking)
admin.site.register(datewise_slot)