from rest_framework import serializers
from accountsetup.models import *
from feeds.models import *
from signals.models import *
from feedback.models import *
from notifications.models import *
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator


User = get_user_model()

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'email',)
        extra_kwargs = {'password': {"write_only": True, 'required': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class Signalserializer(serializers.ModelSerializer):
    class Meta:
        model = Signals
        fields= '__all__'
        depth = 1

class Feedserializer(serializers.ModelSerializer):
    class Meta:
        model = FeedPost
        fields= '__all__'

class OTPserializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = OTPVerification
        fields= '__all__'

class FeedBackserializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackPost
        fields= '__all__'

class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields= '__all__'

class Notificationserializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPost
        fields= '__all__'


class Paymentserializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Payment
        fields= '__all__'

class Subscriptionserializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Subscription
        fields= '__all__'