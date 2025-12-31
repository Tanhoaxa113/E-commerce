# payment/models.py
from django.db import models
from apps.core.models import UUIDModel
from django_fsm import FSMField, transition
from django.utils import timezone

class PaymentTransaction(UUIDModel):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Đang chờ thanh toán'
        SUCCESS = 'SUCCESS', 'Thanh toán thành công'
        FAILED = 'FAILED', 'Thanh toán thất bại'
        REFUNDED = 'REFUNDED', 'Đã hoàn tiền'

    class PaymentProvider(models.TextChoices):
        VNPAY = 'VNPAY', 'Ví VNPAY'
        MOMO = 'MOMO', 'Ví MoMo'
        COD = 'COD', 'Thanh toán khi nhận hàng'

    order = models.ForeignKey(
        'orders.Order',
        related_name='transactions',
        on_delete=models.PROTECT
    )

    txn_ref = models.CharField(max_length=100, unique=True)

    provider_txn_id = models.CharField(max_length=100, blank=True, null=True)
    
    provider_code = models.CharField(
        max_length=20,
        choices=PaymentProvider.choices,
        default=PaymentProvider.VNPAY
    )

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    status = FSMField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    
    @transition(field=status, source=PaymentStatus.PENDING, target=PaymentStatus.SUCCESS)
    def mark_success(self):
        payment_success_at = timezone.now()
    
    @transition(field=status, source=PaymentStatus.PENDING, target=PaymentStatus.FAILED)
    def mark_failed(self):
        payment_failed_at = timezone.now()
    @transition(field=status, source=PaymentStatus.SUCCESS, target=PaymentStatus.REFUNDED)
    def mark_refunded(self):
        payment_refunded_at = timezone.now()
    
    payment_success_at = models.DateTimeField()
    payment_failed_at = models.DateTimeField()
    payment_refunded_at = models.DateTimeField()
    
    description = models.TextField(blank=True, null=True)

    raw_response = models.JSONField(default=dict, blank=True)

    payment_url_created_at = models.DateTimeField(auto_now_add=True)

    payment_processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.provider_code}] {self.txn_ref} - {self.status}"

