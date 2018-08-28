from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class User(AbstractUser):
    """创建用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    _password1 = models.CharField(_("password"), name="password", max_length=128, )

    class Meta:
        db_table = "tb_users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    @property
    def password(self):
        return self._password1

    @password.setter
    def password(self, value):
        if value == "" or value.startswith("pbkdf2_sha256"):
            self._password = value
            self._password1 = value
            return
        self._password1 = make_password(value)
        self._password = value

    def ser_dict(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key) or key == "password":
                setattr(self, key, value)
        return self


