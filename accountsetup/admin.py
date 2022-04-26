from django.contrib import admin
from .models import Payment, Profile, OTPVerification, Subscription



class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','referenceCode','paystackAccessCode', 'paymentFor', 'amount','date','active', 'duration']
    list_per_number = 50
    list_filter = ['user','referenceCode','paystackAccessCode', 'paymentFor', 'amount','date','active', 'duration']
    search_fields = ['user','referenceCode','paystackAccessCode', 'paymentFor', 'amount','date','active', 'duration']

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber','expires_in','active']
    list_per_number = 50
    list_filter = ['subscriber','expires_in','active']
    search_fields = ['subscriber','expires_in','active']

class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user','phonenumber', 'isVerified', 'timestamp']
    list_per_number = 50
    list_filter = ['user','phonenumber',]
    search_fields = ['user','phonenumber',]


admin.site.register(Profile) 
admin.site.register(OTPVerification, OTPVerificationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
