# payment/models.py
from django.db import models
from apps.core.models import UUIDModel 
class PaymentTransaction(UUIDModel):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Đang chờ thanh toán'
        SUCCESS = 'SUCCESS', 'Thanh toán thành công'
        FAILED = 'FAILED', 'Thanh toán thất bại' # Checksum sai, hủy, hoặc lỗi ngân hàng
        REFUNDED = 'REFUNDED', 'Đã hoàn tiền'

    class PaymentProvider(models.TextChoices):
        VNPAY = 'VNPAY', 'Ví VNPAY'
        MOMO = 'MOMO', 'Ví MoMo'
        COD = 'COD', 'Thanh toán khi nhận hàng' # Cash On Delivery

    # Link về đơn hàng gốc
    order = models.ForeignKey(
        'orders.Order', # Dùng string reference để tránh vòng lặp import
        related_name='transactions',
        on_delete=models.PROTECT # Không cho xóa Order nếu đã có giao dịch
    )

    # Mã giao dịch gửi sang VNPAY/MOMO (QUAN TRỌNG NHẤT)
    # Không dùng Order Code trực tiếp, mà phải là: OrderCode + Timestamp hoặc Random
    # Ví dụ: ORDER_ABCXYZ_171628399
    txn_ref = models.CharField(max_length=100, unique=True, help_text="Mã unique gửi sang cổng thanh toán")

    # Mã giao dịch phía Ngân hàng trả về (dùng để đối soát sau này)
    provider_txn_id = models.CharField(max_length=100, blank=True, null=True)
    
    provider_code = models.CharField(
        max_length=20, 
        choices=PaymentProvider.choices,
        default=PaymentProvider.VNPAY
    )

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    status = models.CharField(
        max_length=20, 
        choices=PaymentStatus.choices, 
        default=PaymentStatus.PENDING
    )

    # Nội dung thanh toán (Order description)
    description = models.TextField(blank=True, null=True)

    # Lưu JSON phản hồi thô từ Gateway để debug (Cứu tinh khi lỗi checksum!)
    raw_response = models.JSONField(default=dict, blank=True)
    
    # Thời gian user được chuyển tới trang thanh toán
    payment_url_created_at = models.DateTimeField(auto_now_add=True)
    
    # Thời gian nhận được phản hồi kết quả
    payment_processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.provider_code}] {self.txn_ref} - {self.status}"

