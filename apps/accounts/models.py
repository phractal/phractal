from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nickname = models.CharField("昵称", max_length=128, null=True, help_text="昵称")
    birthday = models.DateField("生日", null=True)
    gender = models.CharField("性别", max_length=16, choices=(("male", "男"), ("female", "女")), default="male")
    address = models.CharField("地址", max_length=128, null=True)
    mobile = models.CharField("电话", max_length=16, null=True)
    avatar = models.TextField("头像", default="avatar/20190716/default.jpg")
    openid = models.CharField("微信openid", max_length=32, null=True)
    headimgurl = models.CharField("头像链接", max_length=256, null=True)
    unionid = models.CharField("微信unionid", max_length=128, null=True)
    global_id = models.IntegerField("全局id")




    class Meta:
        verbose_name_plural = verbose_name = "用户"

    def __repr__(self):
        if self.nickname:
            return self.nickname
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField("验证码", max_length=16, help_text="手机验证码")
    mobile = models.CharField("手机号", max_length=16)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = "短信验证码"

    def __repr__(self):
        return self.code
