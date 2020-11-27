import random
import json
import string

import requests
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.serializers import MobileSerializer, PhoneRegisterSerializer, SimpleRegisterSerializer, UserProfileSerializer
from utils.yunpian import YunPian, IHuyi
from accounts.models import VerifyCode, UserProfile
from wallets.models import MyAccount


from rest_framework_simplejwt.tokens import RefreshToken


from RPC import conDeliverNode


from weixin.client import WeixinAPI

User = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username) | Q(openid=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Test Succeed"}
        return Response(content)




class PhoneMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ 短信验证"""
    serializer_class = MobileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        verify_code = self.generate_code()

        message_status = IHuyi().send_sms(mobile=mobile, code=verify_code)
        message_status = eval(message_status)
        if message_status["code"] != 2:
            return Response({"mobile": message_status["msg"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            VerifyCode.objects.create(mobile=mobile, code=verify_code)


            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)

    @staticmethod
    def generate_code():
        seeds = "1234567890"
        return "".join([random.choice(seeds) for _ in range(6)])


class RegisterViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.request.path == "/register/phone/":
            return PhoneRegisterSerializer
        return SimpleRegisterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data


        # global_id = conDeliverNode.registerAccount(data)

        global_id = 1
        if not global_id:
            return Response("错误", status=status.HTTP_403_FORBIDDEN)
        data['global_id'] = global_id
        serializer = self.get_serializer(data=request.data)
        if isinstance(serializer, PhoneRegisterSerializer):
            password = self.generate_phone_password()
            serializer.initial_data["password"] = password
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response({"token": token}, status=status.HTTP_201_CREATED)
        else:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            MyAccount.objects.create(user=user, balance=0.00)
            return Response("注册成功", status=status.HTTP_201_CREATED)



    def perform_create(self, serializer):
        return serializer.save()

    @staticmethod
    def generate_phone_password(length=16):
        origin_str = string.ascii_letters + string.digits
        return "".join(random.choice(origin_str) for _ in range(length))


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        data = {"id": user.id, "avatar_url": str(user.avatar), "username": user.username, "birthday": user.birthday,
                "address": user.address, "gender": user.gender}
        return Response(data)

    def patch(self, request):
        data = request.data
        base64_file = data.pop("file", None)
        if base64_file:
            data["avatar"] = base64_file
        data_ = data.copy()
        for key in data_.keys():
            if not data_[key]:
                data.pop(key)
        try:
            User.objects.filter(id=self.request.user.id).update_or_create(defaults=data)
            return Response(data)
        except:
            Response({"error": "用户名已存在！"})


class WechatBound(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        user_id = request.query_params.get("state")
        response = requests.get(f"https://api.weixin.qq.com/sns/oauth2/access_token?"
                                f"appid={settings.APP_ID}&"
                                f"secret={settings.API_KEY}&"
                                f"code={code}&"
                                f"grant_type=authorization_code")

        open_id = json.loads(response.text).get("openid")
        if open_id:
            User.objects.filter(id=user_id).update(openid=open_id)
            return HttpResponse("绑定成功！！！")
        else:
            return HttpResponse("绑定失败，请重试")

    def post(self, request):
        user_id = request.data.get("user_id")
        if User.objects.filter(id=user_id, openid__isnull=False).exists():
            return Response({"data": 1}, status=status.HTTP_200_OK)
        else:
            return Response({"data": 0}, status=status.HTTP_200_OK)

class WeiXinQRLogin(APIView):
    def get(self, request):
        APPID = 'wxbb19e286afae10db'
        APPSECRET = '064004a0dd2a8a4c0eeed40975e8907c'
        REDIRECT_URI = 'http://127.0.0.1:8000/authorization'
        SCOPE = 'snsapi_login'
        STATE = 'STATE'
        # REDIRECT_URI = urllib.parse.quote(REDIRECT_URI, safe='/', encoding=None, errors=None)
        redirect_uri = f'https://open.weixin.qq.com/connect/qrconnect?appid={APPID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}&state={STATE}#wechat_redirect'
        return redirect(redirect_uri)

class Authorization(APIView, TokenObtainPairSerializer):
    """
    微信登录扫码后要走的接口
    """
    def get(self, request):
        print(1111111111)
        code = request.GET.get('code')

        print(code)
        api = WeixinAPI(appid="wxbb19e286afae10db",
                        app_secret="064004a0dd2a8a4c0eeed40975e8907c",
                        redirect_uri="http://127.0.0.1:8000/authorization")
        auth_info = api.exchange_code_for_access_token(code=code)
        api = WeixinAPI(access_token=auth_info['access_token'])
        resp = api.user(openid=auth_info['openid'])
        return redirect("http://127.0.0.1:8000/taskpub?nickname={}&headimgurl={}".format(resp["nickname"], resp["headimgurl"]))

        # nickname = resp["nickname"]
        # if UserProfile.objects.filter(openid=resp["openid"]).exists():
        #     user = UserProfile.objects.get(openid=resp["openid"])
        #     id = user.id
        #
        #     class user():
        #         id = id
        #         name = resp["nickname"]
        #         password = 'passwd'
        #
        #     token = self.get_token(user)
        #     print('11111111111111111')
        #     return redirect("http://127.0.0.1:8000/particular?nickname={}&id={}&headimgurl={}&t={}".format(nickname, id, resp["headimgurl"], token))
        # else:
        #     u = UserProfile()
        #     u.openid = resp["openid"]
        #     u.nickname = nickname
        #     u.sex = resp["sex"]
        #     u.headimgurl = resp["headimgurl"]
        #     u.save()
        #     id = u.id
        #     # return Response(resp)
        #     class user():
        #         id = id
        #         name = resp["nickname"]
        #         password = 'passwd'
        #
        #     token = self.get_token(user)
        #     print('2222222222222222222')
        #     return redirect("http://127.0.0.1:8000/particular?nickname={}&id={}&headimgurl={}&t={}".format(resp["nickname"], id, resp["headimgurl"], token))

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token["password"] = user.password
        # ...

        return token