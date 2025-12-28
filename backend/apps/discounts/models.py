from django.db import models
from django.utils import timezone
from apps.core.models import UUIDModel, TimeStampedModel
from apps.users.models import UserProfile
from django.forms import ValidationError

class Coupon(UUIDModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    
    DISCOUNT_TYPES = (
        ('PERCENT', 'Phần trăm'),
        ('AMOUNT', 'Số tiền cố định'),
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    applies_to_brands = models.ManyToManyField('products.Brand', blank=True, related_name='coupons')
    applies_to_products = models.ManyToManyField('products.Product', blank=True, related_name='coupons')
    min_invoice_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Giá trị đơn hàng tối thiểu để áp dụng")
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    max_uses_per_user = models.PositiveIntegerField(default=1)
    
    applies_to_regions = models.ManyToManyField('products.Region', blank=True)
    applies_to_stores = models.ManyToManyField('products.Store', blank=True)
    
    applies_to_customer_type = models.CharField(
        max_length=10,
        choices=UserProfile.CustomerType.choices,
        blank=True,
        null=True,
        help_text="Áp dụng cho loại khách hàng (Để trống nếu áp dụng cho tất cả)"
    )

    def clean(self):
        if self.valid_from and self.valid_until and self.valid_from > self.valid_until:
            raise ValidationError("Ngày kết thúc phải sau ngày bắt đầu.")
        
    def is_applicable_to_user(self, user):
        now = timezone.now()
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        target_type = self.applies_to_customer_type
        if not target_type:
            return True
        profile = getattr(user, 'profile', None)
        if not profile:
            return False
        return profile.customer_type == target_type

    def __str__(self):
        return self.code

class CouponUsage(TimeStampedModel):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='coupon_usages')
