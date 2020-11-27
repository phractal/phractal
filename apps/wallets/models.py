from django.db import models

from django.conf import settings
from tasks.models import Task
from nodes.models import Node

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    task = models.OneToOneField(Task, on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pay_user")
    pay_to_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="pay_to_user")
    created_at = models.DateTimeField("订单生成时间", auto_now_add=True)
    serial_number = models.CharField("流水号", max_length=32, null=True)
    myaccount = models.ForeignKey("MyAccount", on_delete=models.CASCADE)
    amount_money = models.DecimalField("转账金额", max_digits=10, decimal_places=2, blank=True)
    already_pay = models.IntegerField("付款状态", default=0, choices=((0, "未支付"), (1, "支付成功"), (2, "支付失败")))
    pay_at = models.DateTimeField("用户付款时间", null=True)
    wxpay_qrcode = models.TextField("微信付款二维码", null=True)
    alipay_qrcode = models.TextField("支付宝付款二维码", null=True)
    pay_type = models.CharField("付款方式", max_length=16, null=True)

    class Meta:
        verbose_name = "支付记录"
        verbose_name_plural = verbose_name
        ordering = ("created_at",)


class MyAccount(models.Model):
    balance = models.DecimalField("账户余额", max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField("用户付款时间", auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # alipay_account = models.CharField("支付宝账户", max_length=64)
    # bank_card = models.CharField("银行卡账户", max_length=32)

    class Meta:
        verbose_name_plural = verbose_name = "账户记录"


class WithdrawRecord(models.Model):
    amount = models.DecimalField("提现金额", max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField("用户提现时间", auto_now_add=True)
    serial_number = models.CharField("提现流水号", max_length=64)
    account = models.ForeignKey(MyAccount, on_delete=models.CASCADE)
    withdraw_type = models.CharField("提现方式", choices=(("w", "微信"), ("a", "支付宝"), ("b", "银行卡")), default="w",
                                     max_length=16)

    class Meta:
        verbose_name_plural = verbose_name = "提现流水"
