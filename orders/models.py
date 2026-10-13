from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='orders', verbose_name="کاربر")
    order_number = models.CharField(max_length=20, unique=True, verbose_name="شماره سفارش")
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="تلفن")
    address = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="کد پستی")
    total_price = models.IntegerField(verbose_name="مبلغ کل")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                               default='pending', verbose_name="وضعیت")
    payment_id = models.CharField(max_length=100, blank=True, verbose_name="کد پرداخت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, 
                               related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    price = models.IntegerField(verbose_name="قیمت")
    quantity = models.PositiveIntegerField(verbose_name="تعداد")
    size = models.CharField(max_length=20, blank=True, verbose_name="سایز")
    color = models.CharField(max_length=50, blank=True, verbose_name="رنگ")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"