from django.contrib import admin
from vendorsindmsapp.models import (UserRegistration, BasiCompanyInfo, 
CommunicationDetailsCompanyAddress, CommunicationDetailsShippingAddress)

# Register your models here.
admin.site.register([UserRegistration, BasiCompanyInfo, 
CommunicationDetailsCompanyAddress, CommunicationDetailsShippingAddress])