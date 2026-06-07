from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Cake(models.Model):
    FLAVOR_CHOICES = [
        ('chocolate', 'شوكولاتة'),
        ('vanilla', 'فانيليا'),
        ('strawberry', 'فراولة'),
        ('red_velvet', 'ريد فلفت'),
        ('lemon', 'ليمون'),
        ('caramel', 'كراميل'),
    ]

    name = models.CharField(max_length=100, verbose_name='اسم الكعكة')
    flavor = models.CharField(max_length=50, choices=FLAVOR_CHOICES, verbose_name='النكهة')
    description = models.TextField(blank=True, verbose_name='الوصف')
    image = models.ImageField(upload_to='cakes/', blank=True, verbose_name='الصورة')
    catalog_image = models.CharField(max_length=255, blank=True, editable=False)
    is_available = models.BooleanField(default=True, verbose_name='متاحة')

    class Meta:
        verbose_name = 'كعكة'
        verbose_name_plural = 'الكعكات'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def price_per_kg(self):
        catalog_number = None
        if self.id:
            catalog_number = Cake.objects.filter(is_available=True, id__lte=self.id).count()
        return (
            settings.CAKE_SPECIAL_CATALOG_NUMBER_PRICES_PER_KG.get(catalog_number)
            or settings.CAKE_SPECIAL_PRICES_PER_KG.get(self.id)
            or settings.CAKE_SPECIAL_CATALOG_IMAGE_PRICES_PER_KG.get(self.catalog_image)
            or settings.CAKE_PRICE_PER_KG
        )

    @property
    def price_per_kg_display(self):
        return f'{self.price_per_kg:.3f}'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'بانتظار الدفع'),
        ('confirmed', 'مؤكد'),
        ('cancelled', 'ملغي'),
        ('completed', 'مكتمل'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'غير مدفوع'),
        ('paid', 'مدفوع'),
        ('refunded', 'مسترجع'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cake_bookings', verbose_name='المستخدم')
    cake = models.ForeignKey(Cake, on_delete=models.PROTECT, related_name='bookings', verbose_name='الكعكة')
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='الوزن بالكيلو')
    quantity = models.PositiveIntegerField(default=1, verbose_name='الكمية')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name='المبلغ الإجمالي')
    delivery_date = models.DateField(verbose_name='تاريخ الاستلام أو التوصيل')
    delivery_time = models.TimeField(null=True, verbose_name='وقت الاستلام أو التوصيل')
    delivery_address = models.TextField(verbose_name='العنوان')
    cake_message = models.CharField(max_length=100, blank=True, verbose_name='الكتابة على الكعكة')
    special_requests = models.TextField(blank=True, verbose_name='طلبات خاصة')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='حالة الحجز')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid', verbose_name='حالة الدفع')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')

    class Meta:
        verbose_name = 'حجز'
        verbose_name_plural = 'الحجوزات'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.total_price = self.weight_kg * self.quantity * self.cake.price_per_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.cake.name} - {self.total_price}'


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('thawani_omannet', 'ثواني - بطاقات عمان نت والبطاقات البنكية'),
        ('bank_muscat_gateway', 'بوابة بنك مسقط للدفع الإلكتروني'),
        ('oman_bank_transfer', 'تحويل بنكي داخل سلطنة عمان'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment', verbose_name='الحجز')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name='طريقة الدفع')
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='رقم العملية')
    paid_at = models.DateTimeField(default=timezone.now, verbose_name='وقت الدفع')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'دفعة'
        verbose_name_plural = 'المدفوعات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.booking_id} - {self.amount}'
