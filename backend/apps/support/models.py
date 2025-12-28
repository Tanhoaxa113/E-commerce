from django.db import models
from apps.core.models import UUIDModel
from apps.users.models import CustomUser, Staff


class ChatSession(UUIDModel):
    class SessionType(models.TextChoices):
        SALES = 'SALES', 'Tư vấn bán hàng'
        SUPPORT = 'SUPPORT', 'Hỗ trợ kỹ thuật'
        GENERAL = 'GENERAL', 'Hỏi đáp chung'

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    title = models.CharField(max_length=255, default="Cuộc hội thoại mới")
    session_type = models.CharField(max_length=20, choices=SessionType.choices, default=SessionType.SALES)
    
    is_active = models.BooleanField(default=True)
    is_bot_active = models.BooleanField(default=True, help_text="Nếu False, AI sẽ ngừng trả lời để nhân viên chat")
    needs_human_assistance = models.BooleanField(default=False)
    
    context_data = models.JSONField(default=dict, blank=True)
    
    assigned_staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_chats'
    )

    def __str__(self):
        return f"[{self.session_type}] {self.title} - {self.user.username if self.user else 'Guest'}"

class Ticket(UUIDModel):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Thấp'
        MEDIUM = 'MEDIUM', 'Trung bình'
        HIGH = 'HIGH', 'Cao'
        URGENT = 'URGENT', 'Khẩn cấp'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    origin_chat = models.ForeignKey(ChatSession, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')

    status = models.CharField(choices=[('OPEN', 'Mở'), ('IN_PROGRESS', 'Đang xử lý'), ('RESOLVED', 'Đã xong'), ('CLOSED', 'Đóng')], default='OPEN')
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    
    assigned_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')

    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    rating_feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.title}"


class TicketMessage(UUIDModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    
    message = models.TextField()

    product_attachment = models.ForeignKey('products.ProductVariant', on_delete=models.SET_NULL, null=True, blank=True)
    image_attachment = models.ImageField(upload_to='ticket_images/', null=True, blank=True)
    file_attachment = models.FileField(upload_to='ticket_files/', null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        sender = self.staff.user.username if self.staff else (self.user.username if self.user else "Unknown")
        return f"Reply by {sender} in {self.ticket.title}"

class ChatMessage(UUIDModel):
    class SenderType(models.TextChoices):
        USER = 'USER', 'Khách hàng'
        BOT = 'BOT', 'AI Trợ lý'
        STAFF = 'STAFF', 'Nhân viên hỗ trợ'
        SYSTEM = 'SYSTEM', 'Hệ thống'
    
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=SenderType.choices)
    content = models.TextField()
    file_attachments = models.JSONField(default=list, blank=True)

    token_usage = models.PositiveIntegerField(default=0)
    user_feedback = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.content[:20]}..."

class ConsultationLead(UUIDModel):
    STATUS_CHOICES = [
        ('new', 'Mới tiếp nhận'),
        ('processing', 'Đang tư vấn'),
        ('closed_won', 'Đã chốt đơn'),
        ('closed_lost', 'Khách hủy/Không mua'),
    ]

    session = models.OneToOneField(ChatSession, related_name='lead', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    interested_products = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ai_summary = models.TextField(blank=True)
    staff_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Lead: {self.customer_name} - {self.get_status_display()}"