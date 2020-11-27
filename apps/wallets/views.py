from django.shortcuts import render

# Create your views here.
import datetime
import requests
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from .serializers import PaymentSerializer, MyAccountSerializer
from .models import Payment, MyAccount, WithdrawRecord
from rest_framework.permissions import IsAuthenticated
from rest_framework_xml.parsers import XMLParser
from utils.weixin_pay import get_sign, API_KEY
from xml.etree.cElementTree import Element, tostring
from tasks.models import Task
from django.conf import settings
from utils.weixin_withdraw import WeChatWithdraw
from xml.etree import ElementTree as ETree


class PaymentViewSets(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        if self.request.user.is_active:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class MyAccountViewSets(mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    serializer_class = MyAccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = MyAccount.objects.all()
        if self.request.user.is_active:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class WxPayNotifyXMLParser(XMLParser):
    media_type = 'text/xml'


class WxPayNotifyView(APIView):
    parser_classes = (WxPayNotifyXMLParser,)

    def post(self, request):
        xml_data = request.data
        # xml_data = {'appid': 'wx34ab6ee729131856', 'bank_type': 'CFT', 'cash_fee': 1, 'fee_type': 'CNY',
        #             'is_subscribe': 'N',
        #             'mch_id': 1543940791, 'nonce_str': 'JkaKMhNVulUjRmPUfNtZMVCGxGYkUrTc',
        #             'openid': 'ozf5W4zaNCtqg7sHabz4yl6zQwRk', 'out_trade_no': 2240156627936741111063,
        #             'result_code': 'Fail',
        #             'return_code': 'SUCCESS', 'sign': '0D3324FFF87883EAE15264693C44FE9E', 'time_end': 20190820133638,
        #             'total_fee': 1, 'trade_type': 'NATIVE', 'transaction_id': 4200000376201908203371447943}
        return_code = xml_data.get("return_code")
        if return_code == "SUCCESS":
            back_sign = xml_data.pop("sign")
            generate_sign = get_sign(xml_data, API_KEY)
            out_trade_no = xml_data.get("out_trade_no")
            if generate_sign == back_sign:
                instance = Payment.objects.filter(serial_number=out_trade_no).first()
                if instance.already_pay:
                    return Response({"return_code": "SUCCESS", "return_msg": "OK"})
                else:
                    time_end = str(xml_data.get("time_end"))
                    pay_time = time_end[:4] + "-" + time_end[4:6] + "-" + time_end[6:8] + " " + \
                               time_end[8:10] + ":" + time_end[10:12] + ":" + time_end[12:14]
                    total_fee = xml_data.get("total_fee")
                    if total_fee == int(instance.amount_money * 100):
                        task = Task.objects.filter(payment=instance).first()
                        task.status = 2
                        task.save()

                        instance.pay_type = "weixin"
                        instance.already_pay = 1
                        instance.pay_at = pay_time
                        instance.save()
                    return tostring(self.dict_to_xml(d={"return_code": "SUCCESS", "return_msg": "OK"}))
            else:
                instance = Payment.objects.filter(serial_number=out_trade_no).first()
                now = datetime.datetime.now()
                instance.already_pay = 2
                instance.pay_at = now
                instance.save()
                return tostring(self.dict_to_xml(d={"return_code": "SUCCESS", "return_msg": "OK"}))
        else:
            return tostring(self.dict_to_xml(d={"return_code": "SUCCESS", "return_msg": "OK"}))

    @staticmethod
    def dict_to_xml(d, tag="xml"):
        elem = Element(tag)
        for key, val in d.items():
            child = Element(key)
            child.text = str(val)
            elem.append(child)
        return elem


class AliPaymentView(APIView):
    pass


wx_app_id = settings.APP_ID
wx_mch_id = settings.MCH_ID
wx_api_key = settings.API_KEY


class WithdrawView(APIView):
    def post(self, request):
        user = self.request.user
        wechat_openid = user.openid
        if not wechat_openid:
            return Response({"data": "unbound", "content": "对不起，您还未绑定微信，无法使用提现功能!"})
        else:
            amount = request.data.get("amount") or 10000
            obj_withdraw = WeChatWithdraw(wx_app_id, wx_mch_id, wx_api_key)
            nonce_str = obj_withdraw.nonce_str()
            serial_num = obj_withdraw.withdraw_serial_number()
            info = {"mch_appid": wx_app_id,
                    "mchid": wx_mch_id,
                    "nonce_str": nonce_str,
                    "partner_trade_no": serial_num,
                    "openid": wechat_openid,
                    "amount": amount*100,
                    "desc": "个人提现",
                    "spbill_create_ip": "222.93.8.187",
                    "check_name": "NO_CHECK"}

            sign = obj_withdraw.sign(info)
            info.setdefault("sign", sign)
            data = obj_withdraw.to_xml(info)
            response = requests.post(url="https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers",
                                     data=data, cert=())

            # TODO 微信商户退款需要下载双向证书 参考链接：https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=4_3

            res = self.to_dict(response.text)
            if res.get("result_code") == "SUCCESS":
                record = WithdrawRecord.objects.create(amount=amount, account=user.myaccount, serial_number=serial_num)
                myaccount = MyAccount.objects.filter(user=user)
                myaccount.update(balance=F("balance") - amount)
                return Response({"data": "success", "content": "提现成功！"})
            else:
                return Response({"data": "fail", "content": "提现失败，请稍后重试！"})

    @staticmethod
    def to_dict(content):
        raw = {}
        root = ETree.fromstring(content)
        for child in root:
            raw[child.tag] = child.text
        return raw

# https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxb0687587f8196fea&redirect_uri=www.heiyun.com&response_type=code&scope=SCOPE&state=123#wechat_redirect
# http://192.168.3.25:7990/scm/baw/bawangcan-doc.git