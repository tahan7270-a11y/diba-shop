from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="تصویر")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                                blank=True, null=True, related_name='children',
                                verbose_name="دسته والد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                  related_name='products', verbose_name="دسته‌بندی")
    description = models.TextField(verbose_name="توضیحات")
    price = models.IntegerField(verbose_name="قیمت (تومان)")
    discount_price = models.IntegerField(blank=True, null=True, 
                                          verbose_name="قیمت با تخفیف")
    main_image = models.ImageField(upload_to='products/', verbose_name="تصویر اصلی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                 related_name='images', verbose_name="محصول")
    image = models.ImageField(upload_to='products/', verbose_name="تصویر")

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"

    def __str__(self):
        return f"تصویر {self.product.name}"


class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name="سایز")

    class Meta:
        verbose_name = "سایز"
        verbose_name_plural = "سایزها"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام رنگ")
    code = models.CharField(max_length=10, help_text="کد رنگ مثل #FF0000", verbose_name="کد رنگ")

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ‌ها"

    def __str__(self):
        return self.name