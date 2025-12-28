from django.db import models
from apps.core.models import UUIDModel
from django.forms import ValidationError


class Builder (UUIDModel):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

class BuilderItem (UUIDModel):
    class ComponentType(models.TextChoices):
        CPU = 'CPU', ('Vi xử lý')
        GPU = 'GPU', ('Card đồ họa')
        RAM = 'RAM', ('Bộ nhớ trong')
        STORAGE = 'STORAGE', ('Ổ cứng')
        MAINBOARD = 'MAINBOARD', ('Bo mạch chủ')
        PSU = 'PSU', ('Nguồn máy tính')
        CASE = 'CASE', ('Vỏ máy')
        COOLING = 'COOLING', ('Tản nhiệt')
    builder = models.ForeignKey(Builder, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=ComponentType.choices, db_index=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('builder', 'type', 'product_variant')

    def clean(self):
        if self.type == self.ComponentType.CPU:
            existing = BuilderItem.objects.filter(
                builder=self.builder,
                item_type=self.ComponentType.CPU
            ).exclude(id=self.id)
            if existing.exists():
                raise ValidationError("Cấu hình này đã có CPU")

    def get_price(self):
        return self.product_variant.price * self.quantity

