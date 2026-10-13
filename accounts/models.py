from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                                 related_name='profile', verbose_name="کاربر")
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    address = models.TextField(blank=True, verbose_name="آدرس")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="کد پستی")
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name="آواتار")

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"

    def __str__(self):
        return self.user.username