from django import views
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)
from django.views.decorators.csrf import csrf_protect
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

urlpatterns = [
    
    path('rest-auth/facebook/', FacebookLogin.as_view()),
    path('rest-auth/twitter/', TwitterLogin.as_view()),
    path('socialaccounts/', SocialAccountListView.as_view()),
    path('socialaccounts/<int:pk>/disconnect/',SocialAccountDisconnectView.as_view()),
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/github/', TwitterLogin.as_view(), name='github_login'),
    path('verify/<phone>/', getPhoneNumberRegistered.as_view()),
    path('login/', csrf_protect(obtain_auth_token)),
    path('register/', RegisterView.as_view()),
    path('otpverify/', OTPView.as_view()), 
    path('profile/', ProfileView.as_view()),
    path('payment/', PaymentView.as_view()), 
    path('subscription/', SubscriptionView.as_view()), 
    path('changepassword/', ChangePasswordView.as_view()),
    path('devices/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
]
# /api/
