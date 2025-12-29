from django.db import models
from decimal import Decimal
from apps.core.models import TimeStampedModel, UUIDModel, StatusModel, SeoModel
from apps.core.utils import generate_sku
from django.db.models import Sum
from django.utils.text import slugify
from django.core.exceptions import ValidationError
class Brand(StatusModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(UUIDModel,SeoModel):
    class ComponentType(models.TextChoices):
        CPU = 'CPU', 'Vi xử lý'
        GPU = 'GPU', 'Card đồ họa'
        RAM = 'RAM', 'Bộ nhớ trong'
        STORAGE = 'STORAGE', 'Ổ cứng'
        MAINBOARD = 'MAINBOARD', 'Bo mạch chủ'
        PSU = 'PSU', 'Nguồn máy tính'
        CASE = 'CASE', 'Vỏ máy'
        COOLING = 'COOLING', 'Tản nhiệt'
        OTHER = 'OTHER', 'Khác'
    name = models.CharField(max_length=255)
    specifications = models.JSONField(default=dict)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(default="Mô tả sản phẩm")
    type = models.CharField(max_length=20, choices=ComponentType.choices, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    tax_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    category = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_total_stock(self):
        return self.variants.aggregate(total=Sum('stocks__quantity'))['total'] or 0

    def __str__(self):
        return self.name

class ProductVariant(UUIDModel):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=150, unique=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_rate = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    variant_specs = models.JSONField(default=dict)
    name = models.CharField(max_length=255)
    waranty_period_months = models.IntegerField(default=0)

    def clean(self):
        if self.discount_rate > 100:
            raise ValidationError({'discount_rate': 'Giảm giá không được vượt quá 100%.'})
        
    def save(self, *args, **kwargs):
        discount_amount = self.price * (self.discount_rate /100)
        self.final_price = (self.price - discount_amount)
        if not self.sku:
            brand_code = self.product.brand.name[:3]
            type_code = self.product.categories.first().name[:3] if self.product.categories.exists() else "UNK"
            priority_keys = ['model', 'capacity', 'color', 'length', 'height', 'width', 'weight']
            spec_parts = []
            for key in priority_keys:
                val = self.variant_specs.get(key)
                if val:
                    spec_parts.append(str(val))
            spec_code_1 = spec_parts[0] if len(spec_parts) > 0 else "NOSPEC"
            spec_code_2 = spec_parts[1] if len(spec_parts) > 1 else None

            base_sku = generate_sku(
                brand_code=brand_code,
                type_code=type_code,
                spec_code_1=spec_code_1,
                spec_code_2=spec_code_2
            )
            final_sku = base_sku
            counter = 1
            while ProductVariant.objects.filter(sku=final_sku).exists():
                final_sku = f"{base_sku}-{counter}"
                counter += 1
            self.sku = final_sku
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.name} - {self.sku}"


class Category(StatusModel):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='categories')

    def __str__(self):
        return self.name

class ProductImage(UUIDModel):
    variant = models.ForeignKey(ProductVariant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpg')
    alt_text = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.alt_text and self.variant:
            self.alt_text = f"{self.variant.product.name} - {self.variant.sku}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hình ảnh của sản phẩm {self.variant.product.name} ({self.variant.sku})"

class ProductVideo(UUIDModel):
    product = models.ForeignKey(Product, related_name='videos', on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='product_videos/')
    thumbnail = models.ImageField(upload_to='product_video_thumbnails/', null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING', choices=[
        ('PENDING', 'Chờ xử lý'),
        ('PROCESSING', 'Đang xử lý'),
        ('DONE', 'Hoàn thành'),
        ('FAILED', 'Thất bại')
    ])
    hls_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Video for {self.product.name}"

class ProductReview(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Đánh giá bởi {self.user.username} cho sản phẩm {self.product.name}"
    
class ProductComment(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bình luận bởi {self.user.username} của sản phẩm {self.product.name}"
    
class Wishlist(TimeStampedModel):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f"Wishlist của {self.user.username}"
    

class Region(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Store(StatusModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    region = models.ForeignKey(Region, related_name='stores', on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20)
    manager = models.ForeignKey('users.Staff', related_name='managed_stores', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.region.name if self.region else 'No Region'}"
    
class ProductStock(TimeStampedModel):
    variant = models.ForeignKey(ProductVariant, related_name='stocks', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='inventories', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    shelf_location = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('variant', 'store')
        indexes = [
            models.Index(fields=['variant', 'store']),
        ]