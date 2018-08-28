from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """创建用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = "tb_users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


# class Test(AbstractUser):
#     """测试"""
#     _password = models.CharField('password', max_length=30)
#
#     class Meta:
#         db_table = "tb_test"
#         verbose_name = "test"
#         verbose_name_plural = verbose_name
#
#     @property
#     def password(self):
#         return self._password
#
#     @password.setter
#     def password(self, password_input):
#         self._password = self.set_password(password_input)
