from rest_framework import serializers

from django.conf import settings
from .models import MyAccount, Payment

User = settings.AUTH_USER_MODEL


class MyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAccount
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    already_pay = serializers.CharField(source="get_already_pay_display")

    class Meta:
        model = Payment
        fields = "__all__"


class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("pay_qrcode",)
