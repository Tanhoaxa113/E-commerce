from django.contrib import admin
from decimal import Decimal
from .models import Product, ProductVariant, Brand, Category, ProductStock, ProductImage, ProductVideo

class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1
    fields = ('store', 'quantity', 'shelf_location')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)
class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 1
    fields = ('video_file', 'thumbnail', 'duration', 'status', 'hls_url')
    readonly_fields = ('status', 'hls_url', 'duration')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('sku', 'name', 'price', 'is_active')
    readonly_fields = ('sku',)
    inlines = [ProductStockInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'is_active', 'created_at', 'tax_rate' )
    list_filter = ('brand', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('version', 'created_at', 'updated_at')
    inlines = [ProductVariantInline, ProductVideoInline]
    fieldsets = (
        ('Thông tin chung', {
            'fields': ('name', 'brand', 'description', 'specifications', 'tax_rate')
        }),
        ('Cấu hình hệ thống', {
            'classes': ('collapse',),
            'fields': ('is_active', 'version', 'created_at', 'updated_at'),
        }),
    )

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product_name', 'name', 'price', 'waranty_period_months','discount_amount', 'final_price')
    search_fields = ('sku', 'product__name')
    list_filter = ('product__brand',)
    inlines = [ProductStockInline, ProductImageInline]
    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = 'Product'

    def discount_amount(self, obj):
        try:
            return (obj.price * Decimal(obj.discount_rate) / Decimal(100)).quantize(Decimal('0.01'))
        except Exception:
            return None
    discount_amount.short_description = 'Discount Amount'

@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('product_variant_name', 'store', 'quantity', 'updated_at')
    list_filter = ('store', 'variant__product__brand')
    search_fields = ('variant__sku', 'variant__name')

    def product_variant_name(self, obj):
        return f"{obj.variant.product.name} - {obj.variant.name}"
    product_variant_name.short_description = 'Variant'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('version',)