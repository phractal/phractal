import re
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import VerifyCode, UserProfile

User = get_user_model()


class MobileSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        if User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError("用户已存在")

        if not re.match("^1[3578]\d{9}$|^147\d{8}$", mobile):
            raise serializers.ValidationError("非法手机号码")

        one_minute_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(create_time__gt=one_minute_ago).exists():
            raise serializers.ValidationError("距离上一次发送还未超过60s")

        return mobile


class PhoneRegisterSerializer(serializers.ModelSerializer):
    verify_code = serializers.CharField(required=True,
                                        max_length=6,
                                        min_length=6,
                                        write_only=True,
                                        error_messages={
                                            "blank": "请输入验证码",
                                            "required": "请输入验证码",
                                            "max_length": "验证码格式错误",
                                            "min_length": "验证码格式错误",
                                        },
                                        help_text="验证码")

    def validate_verify_code(self, verify_code):
        last_verify_record = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by(
            "-create_time").last()
        if last_verify_record:
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            if five_minutes_ago > last_verify_record.create_time:
                raise serializers.ValidationError("验证码过期")
            if last_verify_record.code != verify_code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码无效")

    def validate(self, attrs):
        """同时对多个字段进行验证"""
        attrs["mobile"] = attrs["username"]
        del attrs["verify_code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "mobile", "verify_code", "password")


class SimpleRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "global_id", "headimgurl", "avatar")


class UserProfileSerializer(serializers.Serializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)


    class Meta:
        field = ("avatar_url",)

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        avatar = obj.avatar.url
        return request.build_absolute_uri(avatar)
