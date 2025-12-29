from django.utils import timezone
from django.db import models
from django.conf import settings
from apps.users.models import UserProfile
from apps.core.models import UUIDModel
from django_fsm import FSMField, transition
import shortuuid
class Order(UUIDModel):
    class OrderStatus(models.TextChoices):
        # Default status
        PENDING = 'PENDING', 'Chờ xác nhận'

        # System status
        PROCESSING = 'PROCESSING', 'Đang xử lý'
        PROCESSING_SUCCESS = 'PROCESSING_SUCCESS', 'Xử lý thành công'
        PROCESSING_FAILED = 'PROCESSING_FAILED', 'Xử lý thất bại'

        # System Failed need MANUAL check
        MANUAL_CHECK = 'MANUAL_CHECK', 'Kiểm tra thủ công'

        # Process completed
        CONFIRMED = 'CONFIRMED', 'Đã xác nhận'

        # Shipping status
        DELIVERING = 'DELIVERING', 'Đang giao hàng'
        DELIVERED = 'DELIVERED', 'Giao thành công'

        # Refund status
        REFUND_REQUESTED = 'REFUND_REQUESTED', 'Đã gửi yêu cầu hoàn tiền'
        REFUNDING = 'REFUNDING', 'Đang hoàn tiền'
        REFUNDED = 'REFUNDED', 'Đã hoàn tiền'

        # Overall Status
        COMPLETED = 'COMPLETED', 'Hoàn thành'
        CANCELED = 'CANCELED', 'Đã hủy'


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    code = models.CharField(max_length=10, unique=True, editable=False)
    
    # FSM Field
    status = FSMField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING, protected=True)

    # --- TRANSITIONS ---

    @transition(field=status, source=OrderStatus.PENDING, target=OrderStatus.PROCESSING)
    def start_processing(self):
        self.processing_at = timezone.now()

    @transition(field=status, source=OrderStatus.PROCESSING, target=OrderStatus.PROCESSING_SUCCESS)
    def processing_passed(self):
        self.processing_success_at = timezone.now()

    @transition(field=status,
                source=[OrderStatus.PROCESSING, OrderStatus.PENDING],
                target=OrderStatus.PROCESSING_FAILED)
    def processing_failed(self, note=None):
        self.processing_failed_at = timezone.now()
        if note:
            # Ghi chú lỗi hệ thống vào order_note để dev xem
            self.order_note = f"{self.order_note or ''}\n[System Error]: {note}"

    @transition(field=status, source=[OrderStatus.PROCESSING_SUCCESS, OrderStatus.MANUAL_CHECK], target=OrderStatus.CONFIRMED)
    def confirm(self):
        self.confirmed_at = timezone.now()

    @transition(field=status, source=OrderStatus.PROCESSING_FAILED, target=OrderStatus.MANUAL_CHECK)
    def manual_check(self): # Đã sửa tên hàm và target
        self.manual_check_at = timezone.now()
    
    # Cancel có thể gọi từ nhiều trạng thái, cập nhật canceled_reason
    @transition(field=status, 
                source=[OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.PROCESSING_SUCCESS, 
                        OrderStatus.PROCESSING_FAILED, OrderStatus.MANUAL_CHECK],
                target=OrderStatus.CANCELED)
    def cancel(self, reason=None):
        self.canceled_at = timezone.now()
        if reason:
            self.canceled_reason = reason

    @transition(field=status, source=OrderStatus.CONFIRMED, target=OrderStatus.DELIVERING)
    def start_delivering(self):
        self.delivering_at = timezone.now()

    @transition(field=status, source=OrderStatus.DELIVERING, target=OrderStatus.DELIVERED)
    def deliver(self):
        self.delivered_at = timezone.now()

    # --- Happy Path: Giao xong -> Hoàn thành (Sau 3 ngày hoặc khách bấm) ---
    @transition(field=status, source=OrderStatus.DELIVERED, target=OrderStatus.COMPLETED)
    def complete(self):
        self.completed_at = timezone.now()

    # --- Refund Path ---
    @transition(field=status, source=OrderStatus.DELIVERED, target=OrderStatus.REFUND_REQUESTED)
    def request_refund(self):
        self.refund_requested_at = timezone.now()

    @transition(field=status, source=OrderStatus.REFUND_REQUESTED, target=OrderStatus.REFUNDING)
    def start_refunding(self):
        self.refunding_at = timezone.now()

    @transition(field=status, source=OrderStatus.REFUNDING, target=OrderStatus.REFUNDED)
    def refund(self):
        self.refunded_at = timezone.now()

    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    canceled_at = models.DateTimeField(null=True, blank=True)
    canceled_reason = models.TextField(null=True, blank=True)

    processing_at = models.DateTimeField(null=True, blank=True)
    processing_success_at = models.DateTimeField(null=True, blank=True)
    processing_failed_at = models.DateTimeField(null=True, blank=True)
    
    manual_check_at = models.DateTimeField(null=True, blank=True)

    delivering_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    refund_requested_at = models.DateTimeField(null=True, blank=True)
    refunding_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    order_note = models.TextField(blank=True, null=True)

    # ... (Các field tiền nong giữ nguyên) ...
    coupon = models.ForeignKey('discounts.Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    discounted_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    applied_customer_type = models.CharField(max_length=20, choices=UserProfile.CustomerType.choices, blank=True, null=True)
    tier_discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    subtotal_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    final_total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = shortuuid.ShortUUID().random(length=8).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Đơn #{self.code} - {self.user.username}"

class OrderAddress(UUIDModel):
    order = models.OneToOneField(Order, related_name='shipping_address', on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    province = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)
    address_line = models.TextField()

    def __str__(self):
        return f"Ship tới: {self.fullname}"

class Fulfillment(UUIDModel):
    class Status(models.TextChoices):
        PREPARING = 'PREPARING', 'Đang đóng gói'
        READY_TO_PICK = 'READY_TO_PICK', 'Chờ lấy hàng'
        SHIPPED = 'SHIPPED', 'Đang vận chuyển'
        DELIVERED = 'DELIVERED', 'Giao thành công'
        RETURNED = 'RETURNED', 'Đã hoàn hàng'
        FAILED = 'FAILED', 'Giao thất bại'

    order = models.ForeignKey(Order, related_name='fulfillments', on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    shipping_carrier = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PREPARING)

    tracking_url = models.URLField(max_length=500, blank=True, null=True)

    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Vận đơn {self.tracking_number or 'Mới'}"

class DeliveryAttempt(UUIDModel):
    class AttemptStatus(models.TextChoices):
        FAILED = 'FAILED', 'Giao không thành công'
        RESCHEDULED = 'RESCHEDULED', 'Đã hẹn lại lịch'

    class FailureReason(models.TextChoices):
        CUSTOMER_BUSY = 'CUSTOMER_BUSY', 'Khách bận/Hẹn lại'
        UNREACHABLE = 'UNREACHABLE', 'Khách không nghe máy'
        WRONG_ADDRESS = 'WRONG_ADDRESS', 'Sai thông tin/Địa chỉ'
        REFUSED = 'REFUSED', 'Khách từ chối nhận hàng'
        OTHER = 'OTHER', 'Lý do khác (Thời tiết,...)'

    fulfillment = models.ForeignKey(
        Fulfillment,
        related_name='delivery_attempts',
        on_delete=models.CASCADE
    )
    
    status = models.CharField(max_length=20, choices=AttemptStatus.choices)
    reason = models.CharField(max_length=50, choices=FailureReason.choices, blank=True, null=True)

    note = models.TextField(blank=True, null=True)
    
    attempted_at = models.DateTimeField(auto_now_add=True)
    rescheduled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Lần giao #{str(self.id)[:8]} - {self.get_reason_display()}"

class PaymentTransaction(UUIDModel):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Đang xử lý'
        SUCCESS = 'SUCCESS', 'Thành công'
        FAILED = 'FAILED', 'Thất bại'
        REFUNDED = 'REFUNDED', 'Đã hoàn tiền'

    order = models.ForeignKey(Order, related_name='transactions', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    gateway_response = models.JSONField(default=dict, blank=True)

class OrderItem(UUIDModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.ProductVariant', on_delete=models.PROTECT)

    product_name_snapshot = models.CharField(max_length=255)
    sku_snapshot = models.CharField(max_length=50, blank=True, null=True)
    
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    total_line_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.final_price
        if not self.product_name_snapshot:
            self.product_name_snapshot = str(self.product)
        
        if not self.sku_snapshot and hasattr(self.product, 'sku'):
            self.sku_snapshot = self.product.sku

        if self.price and self.quantity:
            self.total_line_amount = self.price * self.quantity
        else:
            self.total_line_amount = 0
            
        super().save(*args, **kwargs)

