# from __future__ import absolute_import, unicode_literals
import http.client
import math
import random

from django.core.exceptions import ObjectDoesNotExist
from mailjet_rest import Client
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView

from .models import BankDetails
from .models import BasiCompanyInfo
from .models import CommunicationDetailsCompanyAddress
from .models import CommunicationDetailsShippingAddress
from .models import LegalInformation
from .models import UserRegistration


class RegistrationView(APIView):
    def post(self, request):
        try:
            data = request.data
            user = UserRegistration.objects.create_user(full_name=data['fullname'],
                                                 password=data['password'],
                                                 user_country=data['country'],
                                                 user_location=data['location'],
                                                 company_name=data['company_name'],
                                                 user_phoneno=data['phone'],
                                                 username=data['mail'],
                                                 usertype=data['usertype'])
            user_info = {
                'user_id':user.pk,
                'user_fullname':user.full_name,
                'company_name':user.company_name,
                'user_mail':user.user_mail}
            return Response({'status': 201, 'message': 'user signed up successfully','data':user_info}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def login(request):
    data = request.data

    try:
        user = UserRegistration.objects.get(username=data['mail'])
        if user.is_active:
            b = user.check_password(data['password'])
            user_info = {
                'user_id': user.id,
                'username': user.username,
                'company_name': user.company_name,
                'mail': user.user_mail,
                'phone': user.user_phoneno}
            if b:
                return Response({'status': 200, 'message': 'user login successfully',
                                 'user_info': user_info}, status=200)

            else:
                return Response({'status': 404, 'message': 'user not found'}, status=404)
        else:
            return Response({'status': 404, 'message': 'your account does not exists'}, status=404)
    except ObjectDoesNotExist:
        return Response({'status': 404, 'error': "email not present please check email you entered"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def phoneotpchangepassword(request):
    data = request.data
    digits = "0123456789"

    number = data['mphone']
    # user=userregistration.objects.get(phone=number)
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    try:
        user = UserRegistration.objects.get(user_phoneno=number)

        conn = http.client.HTTPSConnection("global.datagenit.com")
        headers = {'cache-control': "no-cache"}
        conn.request("GET", "/API/sms-api.php?auth=D!~782hRDggf0h5m&senderid=Vendor&msisdn=" + str(
            number) + "&message=OTP:" + str(OTP), headers=headers)
        res = conn.getresponse()
        user.user_otp = OTP
        user.save()

        return Response({'status': 200, 'message': 'OTP sent successfully'}, status=200)

    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "phone number not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def emailforgotpassword(request):
    data = request.data
    recemail = data['email']
    link = "www.vendorsin.com"
    try:
        user = UserRegistration.objects.get(user_mail=recemail)
        if user:
            api_key = '760b42c43a3522e91e004257a100d97e'
            api_secret = 'a789bad80219938e51485b2d53db68d3'
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')
            data1 = {'Messages': [
                {"From": {"Email": "admin@vendorsin.com", "Name": "Vendors In"}, "To": [{"Email": recemail}],
                 "Subject": "Password Change",
                 "TextPart": "Dear User,\n\nclick link here to change password: " + link + "\n\nThis is System Generated Email Please Don't Reply For This Mail"}]}
            result = mailjet.send.create(data=data1)
            if result.status_code == 200:
                return Response({'status': 200, 'message': 'mail sent successfully'}, status=200)

            else:
                return Response({'status': 424, 'message': 'mail not sent'}, status=424)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "email not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def emailverification(request):
    data = request.data
    digits = '0123456789'
    recemail = data['email']
    try:
        user = UserRegistration.objects.get(user_mail=recemail)
        if user:
            api_key = '760b42c43a3522e91e004257a100d97e'
            api_secret = 'a789bad80219938e51485b2d53db68d3'
            OTP = ""
            for i in range(4):
                OTP += digits[math.floor(random.random() * 10)]
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')
            data1 = {'Messages': [
                {"From": {"Email": "admin@vendorsin.com", "Name": "Vendors In"}, "To": [{"Email": recemail}],
                 "Subject": "OTP Confirmation",
                 "TextPart": "Dear User,\n\nYour OTP is: " + OTP + "\n\nThis is System Generated Email Please Don't Reply For This Mail"}]}
            result = mailjet.send.create(data=data1)
            if result.status_code == 200:
                user.user_otp = OTP
                user.save()
                return Response({'status': 200, 'message': 'mail sent successfully'}, status=200)

            else:
                return Response({'status': 424, 'message': 'mail not sent'}, status=424)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "email not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def phoneotpcheck(request):
    data = request.data
    otp = data['otp']
    try:
        user = UserRegistration.objects.get(user_otp=otp)
        if user:
            newpassword = data['password']
            user.set_password(newpassword)
            user.save()
            return Response({'status': 200, 'message': 'password updated successfully'}, status=200)
        else:
            return Response({'status': 424, 'message': 'otp/phone not exist'}, status=200)
    except ObjectDoesNotExist as e:
        return Response({'status': 404, 'error': "otp not exist"}, status=404)
    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def changepassword(request):
    data = request.data
    try:
        user = UserRegistration.objects.get(user_mail=data['email'])
        b = user.check_password(data['password'])
        if b:
            newpassword = data['newpassword']
            user.set_password(newpassword)
            user.save()
            return Response({'status': 200, 'message': 'password updated successfully'}, status=200)
        else:
            return Response({'status': 424, 'message': 'password not match'}, status=200)

    except Exception as e:
        return Response({'status': 500, 'error': str(e)}, status=500)


class VendorWorkflowAPI(APIView):

    def get(self, request):
        data = request.data
        try:
            if data['tab_name'] == 'basic_company_info':
                basic_company_info = BasiCompanyInfo.objects.get(user_id=data['user_id'])
                basic_company_info = {
                    'company_code': basic_company_info.company_code,
                    'company_name': basic_company_info.company_name,
                }
                return Response({'data': basic_company_info, 'status': 200}, status=200)
            # elif :
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)
        # provide existing data for edit

    def post(self, request):
        data = request.data
        tab_name = data['tab_name']
        try:
            if tab_name == 'Basic_Company_Info':
                # return Response({'status':400, 'error':'invalid tab_name'}, status=400)
                create_basic_company_info(data)
            elif tab_name == 'Communication_Details':
                create_communication_details(data)
            elif tab_name == 'bank_details':
                create_bankdetails(data)
            elif tab_name == 'supply_industries':
                create_supply_industries(data)
            elif tab_name == 'legal_info':
                create_legal_info(data)
            else:
                return Response({'status': 400, 'error': 'invalid tab_name'}, status=400)
            return Response({'status': 201, 'message': 'success'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)
            # return 500

    def put(self, request):
        data = request.data
        tab_name = data['tab_name']
        try:
            if tab_name == 'Basic_Company_Info':
                update_basic_company_info(data)
            elif tab_name == 'Communication_Details':
                create_communication_details(data)
            elif tab_name == 'bank_details':
                create_bankdetails(data)
            elif tab_name == 'supply_industries':
                create_supply_industries(data)
            elif tab_name == 'legal_info':
                create_legal_info(data)
            else:
                return Response({'status': 400, 'error': 'invalid tab_name'}, status=400)
            return Response({'status': 201, 'message': 'success'}, status=201)

        except Exception as e:
            pass


def create_basic_company_info(data):
    # data['company_code']
    # BasicCompany.
    company_code = generate_company_code()
    BasiCompanyInfo.objects.create(company_code=company_code,
                                   company_name=data['companyname'],
                                   company_type=data['companytype'],
                                   tax_payer_type=data['taxpayertype'],
                                   registration_date=data['registrationdate'],
                                   buziness_country=data['buzinesscountry'],
                                   buziness_currency=data['buzinesscurrency'],
                                   buziness_type=data['buzinesstype'],
                                   msme_registered=data['msme_registered'],
                                   gst_no=data['gstno'],
                                   pan_no=data['panno'],
                                   created_by_id=data['createdby'],
                                   updated_by_id=data['updatedby'],
                                   user_id = UserRegistration.objects.get(id=data['user_id']),
                                   nature_of_buziness=data['natureofbuz'])

    return Response({'status': 201,
                     'company_code': company_code,
                     'message': 'user signed up successfully'}, status=201)


def create_communication_details(data):
    CommunicationDetailsCompanyAddress.objects.create(company_name=data['companyname'],
                                                      country=data['country'],
                                                      state=data['state'],
                                                      city=data['city'],
                                                      pincode=data['pincode'],
                                                      landmark=data['landmark'],
                                                      address=data['address'],
                                                      website=data['website'],
                                                      mail_id=data['mail_id'],
                                                      telephone=data['telephone'],
                                                      mobile=data['mobile'])

    CommunicationDetailsShippingAddress.objects.create(shipping_company_name=data['scompanyname'],
                                                       shipping_country=data['scountry'],
                                                       shipping_state=data['sstate'],
                                                       shipping_city=data['scity'],
                                                       shipping_pincode=data['spincode'],
                                                       shipping_landmark=data['slandmark'],
                                                       shipping_address=data['saddress'],
                                                       shipping_mail_id=data['smail_id'],
                                                       shipping_telephone=data['stelephone'],
                                                       shipping_mobile=data['smobile'])

    return Response({'status': 201, 'message': 'company details added successfully'}, status=201)


def create_bankdetails(data):
    BankDetails.objects.create(acc_holder_name=data['acc_holder_name'],
                               type_account=data['type_account'],
                               bank_name=data['bank_name'],
                               account_no=data['account_no'],
                               ifsc_code=data['ifsc_code'],
                               branch=data['branch'],
                               transfer_type=data['transfer_type'],
                               swift_code=data['swift_code'],
                               micr_no=data['micr_no'],
                               iban_code=data['iban_code'],
                               created_by_id=data['created_by_id'],
                               updated_by_id=data['updated_by_id'])

    return Response({'status': 201, 'message': 'company details added successfully'}, status=201)


def create_supply_industries(data):
    pass


def create_legal_info(data):
    pass


def update_basic_company_info(data):
    try:
        user = BasiCompanyInfo.objects.get(company_code=data['company_code'])
        user.company_name = data['company_name']
        user.company_type = data['company_type']
        user.tax_payer_type = data['tax_payer_type']
        user.registration_date = data['registration_date']
        user.buziness_country = data['buziness_country']
        user.buziness_currency = data['buziness_currency']
        user.buziness_type = data['buziness_type']
        user.msme_registered = data['msme_registered']
        user.gst_no = data['gst_no']
        user.pan_no = data['pan_no']
        user.nature_of_buziness = data['nature_of_buziness']
        user.save()
        return Response({'status': 200, 'message': 'company details updated successfully'}, status=200)
    except Exception as e:
        return Response({'status': 404, 'error': str(e)}, status=404)


def update_communication_details(data):
    pass


def update_bankdetails(data):
    pass


def update_supply_industries(data):
    pass


def update_legal_info(data):
    pass


class fileuploadapi(APIView):

    def post(self, request):
        data = request.data
        file = data['upload_document']
        # import io
        # io_string = io.StringIO(decoded_file)
        # binary_data=open(io_string, 'rb')
        # with open(path, 'rb') as f:
        # contents = f.read()
        LegalInformation.objects.create(document_name=data['document_name'],
                                        registered_date=data['registered_date'],
                                        valid_till=data['valid_till'],
                                        upload_document=file, document=file.read())

        '''directory = "Documents"
        parent_dir = "E:\\users"
        path = os.path.join(parent_dir, directory)
        fs = FileSystemStorage(path)
        try:
                os.mkdir(path) 
                print("Directory '% s' created" % directory)
                # for count, x in enumerate(request.FILES.getlist("files")):
                #         print(count)
                #         print(x)
                
        except OSError:
                print("folder exist.....") 
                fs.save(doc.name,doc)'''
        return Response({'status': 200, 'message': 'file uploaded'}, status=200)

    def get(self, request):
        legalinfo_obj = LegalInformation.objects.get(id=13)
        print(legalinfo_obj.document)
        # f = open('E:\\users\\Documents\\test.xlsx', 'wb')
        from django.conf import settings
        f = open(settings.BASE_DIR+'\\documents', 'wb')

        f.write(legalinfo_obj.document)
        document_path = "http://127.0.0.1:8000/documents/"+document_name

        return Response({'status': 200, 'document_path':document_path,'message': 'file uploaded'}, status=200)


def generate_company_code():
    basic_info_obj = BasiCompanyInfo.objects.last()
    return int(basic_info_obj.company_code) + 1
