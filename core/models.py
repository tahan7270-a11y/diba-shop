from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    image = models.ImageField(upload_to='banners/', verbose_name="تصویر")
    link = models.URLField(blank=True, null=True, verbose_name="لینک")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.IntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "بنر"
        verbose_name_plural = "بنرها"
        ordering = ['order']

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="مزون دیبا", verbose_name="نام سایت")
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    address = models.TextField(blank=True, verbose_name="آدرس")
    instagram = models.URLField(blank=True, verbose_name="اینستاگرام")
    telegram = models.URLField(blank=True, verbose_name="تلگرام")
    whatsapp = models.URLField(blank=True, verbose_name="واتساپ")

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return self.site_name