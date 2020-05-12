from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class UserProfile(AbstractUser):
    phone = models.CharField(max_length=11,default='',verbose_name=u'手机号')
    birthday = models.DateField(null=True, blank=True,verbose_name=u'生日')
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="male")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/2020/03/touxiang.jpg", max_length=100)
    email = models.EmailField(max_length=20,null=True, blank=True,verbose_name=u'邮箱')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", choices=(("register",u"注册"),("forget",u"找回密码"), ("update_email",u"修改邮箱")), max_length=30)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=timezone.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)