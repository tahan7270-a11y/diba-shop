from django.db import models
from django.contrib.auth.models import User


class AIRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('processing', 'در حال پردازش'),
        ('done', 'انجام شده'),
        ('failed', 'ناموفق'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    user_image = models.ImageField(upload_to='ai_input/', verbose_name="عکس کاربر")
    product_image = models.ImageField(upload_to='ai_input/', verbose_name="عکس محصول")
    result_image = models.ImageField(upload_to='ai_output/', 
                                      blank=True, null=True, verbose_name="عکس نتیجه")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                               default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "درخواست AI"
        verbose_name_plural = "درخواست‌های AI"
        ordering = ['-created_at']

    def __str__(self):
        return f"درخواست {self.id} - {self.user.username}"