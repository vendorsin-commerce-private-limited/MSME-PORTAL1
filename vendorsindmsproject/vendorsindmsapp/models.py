from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserRegistration(AbstractUser):
    # username = models.CharField(max_length=30,unique=False)
    full_name = models.CharField(max_length=50)
    # USERNAME_FIELD = 'user_mail'
    user_country = models.BigIntegerField(null=True)
    # user_mail=models.CharField(max_length=100,unique=True)
    user_phoneno = models.CharField(max_length=15, unique=True)
    usertype = models.BigIntegerField(null=True)
    user_location = models.TextField(null=True)
    company_name = models.CharField(max_length=20)
    user_otp = models.CharField(max_length=6, null=True)
    class Meta:
        db_table = "UserRegistration"


class BasiCompanyInfo(models.Model):
    basic_company_info_id = models.BigAutoField(primary_key=True)
    company_code = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    company_type = models.BigIntegerField()
    tax_payer_type = models.BigIntegerField()
    registration_date = models.DateTimeField()
    buziness_country = models.BigIntegerField()
    buziness_currency = models.BigIntegerField()
    buziness_type = models.CharField(max_length=20)
    msme_registered = models.BooleanField()
    gst_no = models.CharField(max_length=20)
    pan_no = models.CharField(max_length=10)
    # tax_no=models.CharField(max_length=30)
    # vat_no=models.CharField(max_length=15)
    nature_of_buziness = models.BigIntegerField()
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)

    created_by_id = models.BigIntegerField()  # user_id
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by_id = models.BigIntegerField()

    class Meta:
        db_table = "BasiCompanyInfo"


class CommunicationDetailsCompanyAddress(models.Model):
    company_name = models.CharField(max_length=50)
    country = models.BigIntegerField()
    state = models.BigIntegerField()
    city = models.BigIntegerField()
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    website = models.CharField(max_length=20)
    mail_id = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)

    # created_by_id = models.BigIntegerField() #user_id
    # created_on = models.DateTimeField(auto_now_add=True)
    # updated_on = models.DateTimeField(auto_now=True)
    # updated_by_id = models.BigIntegerField()

    class Meta:
        db_table = "CommunicationDetailsCompanyAddress"


class CommunicationDetailsShippingAddress(models.Model):
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    shipping_company_name = models.CharField(max_length=50)
    shipping_country = models.BigIntegerField()
    shipping_state = models.BigIntegerField()
    shipping_city = models.BigIntegerField()
    shipping_pincode = models.CharField(max_length=10)
    shipping_landmark = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=100)
    shipping_mail_id = models.CharField(max_length=50)
    shipping_telephone = models.CharField(max_length=15)
    shipping_mobile = models.CharField(max_length=15)
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)

    # created_by_id = models.BigIntegerField() #user_id
    # created_on = models.DateTimeField(auto_now_add=True)
    # updated_on = models.DateTimeField(auto_now=True)
    # updated_by_id = models.BigIntegerField()

    class Meta:
        db_table = "CommunicationDetailsShippingAddress"


class ContactDetails(models.Model):
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    dept = models.BigIntegerField()
    designation = models.BigIntegerField()
    contact_no = models.CharField(max_length=15)
    mobile_no = models.CharField(max_length=15)
    mail_id = models.CharField(max_length=30)


    # created_by_id = models.BigIntegerField() #user_id
    # created_on = models.DateTimeField(auto_now_add=True)
    # updated_on = models.DateTimeField(auto_now=True)
    # updated_by_id = models.BigIntegerField()

    class Meta:
        db_table = "Contact_Details"


class BankDetails(models.Model):
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    acc_holder_name = models.CharField(max_length=30)
    type_account = models.CharField(max_length=30)
    bank_name = models.CharField(max_length=30)
    account_no = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=25)
    branch = models.CharField(max_length=20)
    transfer_type = models.CharField(max_length=20)
    swift_code = models.CharField(max_length=25)
    micr_no = models.CharField(max_length=25)
    iban_code = models.CharField(max_length=25)
    created_by_id = models.BigIntegerField()  # user_id
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by_id = models.BigIntegerField()


    class Meta:
        db_table = "BankDetails"


class LegalInformation(models.Model):
    user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=20)
    registered_date = models.DateField()
    valid_till = models.DateField()
    upload_document = models.FileField()
    # aadhar_document = models.BinaryField(null=True)

    class Meta:
        db_table = "LegalInformation"

# {
#     "document_type":"aadhar" #pan, 
#     "file":
#     "document_name"
# }
