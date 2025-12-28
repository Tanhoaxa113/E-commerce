from django.db import models
from django.conf import settings
from django.forms import ValidationError
from apps.core.models import UUIDModel, TimeStampedModel, StatusModel


class Cart(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)

    def clean(self):
        if self.user and self.session_key:
            raise ValidationError("Giỏ hàng không thể vừa liên kết với User vừa có Session Key.")
        if not self.user and not self.session_key:
            raise ValidationError("Giỏ hàng phải liên kết với User hoặc có Session Key.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], condition=models.Q(user__isnull=False), name='unique_user_cart')
        ]
    def __str__(self):
        return f"Giỏ hàng của {self.user.username}"
    
class CartItem(UUIDModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} trong giỏ hàng của {self.cart.user.username}"
