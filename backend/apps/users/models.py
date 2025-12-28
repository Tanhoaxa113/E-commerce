from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import UUIDModel
from unidecode import unidecode
from uuid6 import uuid7

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid7
    )
    email = models.EmailField(unique=True)
    invalid_try = models.IntegerField(default=0)
    otp = models.CharField(max_length=8, blank=True, null=True)
    otp_valid_until = models.DateTimeField(null=True)
    is_banned = models.BooleanField(default=False)
    banned_until = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return self.username

class UserProfile(UUIDModel):
    class CustomerType(models.TextChoices):
        BRONZE = 'BRONZE', 'Bronze'
        SILVER = 'SILVER', 'Silver'
        GOLD = 'GOLD', 'Gold'
        PLATINUM = 'PLATINUM', 'Platinum'
        DIAMOND = 'DIAMOND', 'Diamond'

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    customer_type = models.CharField(
        max_length=10,
        choices=CustomerType.choices,
        default=CustomerType.BRONZE)
    loyalty_points = models.PositiveIntegerField(default=0, help_text="Điểm tích lũy để thăng hạng")

    def __str__(self):
        return f"Profile of {self.user.username}"

class Staff(UUIDModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(blank=True, null=True, max_length=100)
    hire_date = models.DateField(blank=True,null=True, default=timezone.now)
    work_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position}"
    
class HistorySearch(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid7
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    result_count = models.IntegerField(default=0)
    content_no_accent = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.content:
            clean_text = self.content.lower()
            clean_text = " ".join(clean_text.split())
            self.content = clean_text
            self.content_no_accent = unidecode(self.content)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} tìm kiếm '{self.content}' vào {self.timestamp}"

class UserActivity(UUIDModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    category = models.ForeignKey('products.Category', on_delete=models.CASCADE)
    action_type = models.CharField(choices=[('VIEW', 'Xem'), ('CART', 'Thêm giỏ'), ('BUY', 'Mua')])
    timestamp = models.DateTimeField(auto_now_add=True)

