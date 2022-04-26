from datetime import date
from api.serializer import Notificationserializer
from .models import *
from django.utils import formats
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


class NotificationView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        start_date = user.date_joined

        notifications = NotificationPost.objects.filter(date__gte=start_date)
        serializer = Notificationserializer(notifications, many = True)
        return Response(serializer.data)
