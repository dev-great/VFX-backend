import base64
from api.serializer import Paymentserializer, Subscriptionserializer, Profileserializer, OTPserializer, ChangePasswordSerializer
from .models import *
from datetime import datetime
from rest_framework import generics
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from .models import OTPVerification
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from api.serializer import Userserializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.utils.decorators import method_decorator


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class getPhoneNumberRegistered(APIView):
    
    @staticmethod
    def get(request, phone):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        user_email = user.email
        user_nameF = user.first_name
        user_nameL = user.last_name
        try:
            phonenumber = OTPVerification.objects.get(phonenumber=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            OTPVerification.objects.create(
                phonenumber=phone,
            )
            phonenumber = OTPVerification.objects.get(phonenumber=phone)  # user Newly created Model
        phonenumber.counter += 1  # Update Counter At every Call
        phonenumber.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(phonenumber.counter))
        msg = f'DO NOT DISCLOSE. Dear {user_nameF} {user_nameL}, The OTP for your confirmation is : {OTP.at(phonenumber.counter)} to verify {phonenumber}. Thank you for choosing VFX.'
        send_mail('VFX OTP Verification', msg, settings.EMAIL_HOST_USER,
        [user_email], fail_silently=False)
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.at(phonenumber.counter)}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            phonenumber = OTPVerification.objects.get(phonenumber=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  
        
                # HOTP Model
        if OTP.verify(request.data["otp"], phonenumber.counter):  # Verifying the OTP
            phonenumber.isVerified = True
            phonenumber.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)

class OTPView(APIView, ):

        def get_serializer_class(self):
            return OTPserializer


        csrf_protect_method = method_decorator(csrf_protect)
        def post(self, request):
            username = request.user.username
            user = User.objects.get(username__exact=username)

            serializers = OTPserializer(data=request.data)
            if serializers.is_valid():
                serializers.save(user=user)
                return Response(serializers.data)
            return Response(OTPserializer)
        

class PaymentView(APIView, ):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def get_serializer_class(self):
        return Paymentserializer

    def get(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        detail = user.username

        paymentHistory = Payment.objects.filter(user=user)
        serializer = Paymentserializer(paymentHistory, many = True)
        return Response(serializer.data)


    csrf_protect_method = method_decorator(csrf_protect)
    def post(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)

        serializers = Paymentserializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=user)
            return Response(serializers.data)
        return Response(Paymentserializer)
        

class SubscriptionView(APIView, ):

        def get_serializer_class(self):
            return Subscriptionserializer


        csrf_protect_method = method_decorator(csrf_protect)
        def post(self, request):
            username = request.user.username
            user = User.objects.get(username__exact=username)

            serializers = Subscriptionserializer(data=request.data)
            if serializers.is_valid():
                serializers.save(user=user)
                return Response(serializers.data)
            return Response(Subscriptionserializer)
        

class ProfileView(APIView, ):

        def get_serializer_class(self):
            return Profileserializer
        
        def get(self, request):
            username = request.user.username
            user = User.objects.get(username__exact=username)
            detail = user.username

            profile = Profile.objects.filter(user=user)
            serializer = Profileserializer(profile, many = True)
            return Response(serializer.data)


        csrf_protect_method = method_decorator(csrf_protect)
        def post(self, request):
            username = request.user.username
            user = User.objects.get(username__exact=username)

            serializers = Profileserializer(data=request.data)
            if serializers.is_valid():
                serializers.save(user=user)
                return Response(serializers.data)
            return Response(Profileserializer)
        

class RegisterView(APIView):
    csrf_protect_method = method_decorator(csrf_protect)
    
    def post(self, request):
        serializers = Userserializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"error": False})
        return Response({"error": True})



class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)