from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from datetime import timedelta
from datetime import datetime as dt

today = datetime.date.today()
# Create your models here.

class Profile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    profilepix= models.ImageField(upload_to="profile/")


    def __str__(self) :
        return self.user.username


class OTPVerification(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    phonenumber= models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    referenceCode = models.CharField(max_length=100, default='', blank=True)
    paystackAccessCode = models.CharField(max_length=100, default='', blank=True)
    paymentFor = models.CharField(max_length=100, default='', blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    duration = models.PositiveBigIntegerField(default=30)


    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Payment)
def create_subscription(sender, instance, *args, **kwargs):
	if instance:
		Subscription.objects.create(subscriber=instance, expires_in=dt.now().date() + timedelta(days=instance.duration))


#### User Subscription
class Subscription(models.Model):
    subscriber = models.ForeignKey(Payment, related_name='subscription', on_delete=models.CASCADE, default=None)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
      return self.subscriber.user.username

@receiver(post_save, sender=Subscription)
def update_active(sender, instance, *args, **kwargs):
	if instance.expires_in < today:
		subscription = Subscription.objects.get(id=instance.id)
		subscription.delete()
