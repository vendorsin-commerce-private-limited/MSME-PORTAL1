
class RegistrationView(APIView):
    def post(self, request):
        try:
            data = request.data
            # print("post_method")
            # user_obj=registration.objects.get(username='harish')
            # b =user_obj.check_password("12345")

            # user=userregistration.objects.filter(username=data['mail'])

            # if user:
            #     return Response({'status':400, 'errors':"User already exists.Try with other username"}, status=400)
            UserRegistration.objects.create_user(username=data['fullname'],
                                                 password=data['password'],
                                                 user_country=data['country'],
                                                 user_location=data['location'],
                                                 company_name=data['company_name'],
                                                 user_phoneno=data['phone'],
                                                 user_mail=data['mail'],
                                                 usertype=data['usertype'])
            # user_info = {
            #     'user_id':user.pk,
            #     'user_fullname':user.full_name,
            #     'company_name':user.company_name,
            #     'user_mail':user.user_mail}
            return Response({'status': 201, 'message': 'user signed up successfully'}, status=201)
        except Exception as e:
            return Response({'status': 500, 'error': str(e)}, status=500)


@api_view(['post'])
def login(request):
    data = request.data

    try:
        user = UserRegistration.objects.get(user_mail=data['mail'])
        b = user.check_password(data['password'])
        user_info = {
            'user_id': user.id,
            'username': user.username,
            'company_name': user.company_name,
            'mail': user.user_mail}
        if b:
            return Response({'status': 200, 'message': 'user login successfully',
                             'user_info': user_info}, status=200)

        else:
            return Response({'status': 404, 'message': 'user not found'}, status=404)
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
    for i in range(6):
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
