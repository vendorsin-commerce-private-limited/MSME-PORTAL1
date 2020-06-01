from django.contrib import admin
from django.urls import path
from .views import RegistrationView
from .views import VendorWorkflowAPI
from .views import fileuploadapi
from .views import login
from .views import phoneotpchangepassword
from .views import emailverification
from .views import emailforgotpassword
from. views import phoneotpcheck
from .views import changepassword

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('usertypesignup/',VendorWorkflowAPI.as_view()),
    path('documentupload/',fileuploadapi.as_view()),
    path('login/',login),
    path('phoneotpchangepassword/',phoneotpchangepassword),
    path('emailforgotpassword/',emailforgotpassword),
    path('emailverification/',emailverification),
    path('phoneotpcheck/',phoneotpcheck),
    path('changepassword/',changepassword)

]