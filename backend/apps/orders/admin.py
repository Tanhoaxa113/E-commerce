from django.contrib import admin
from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'total_line_amount')
    readonly_fields = ('total_line_amount',)

class OrderAddressInline(admin.StackedInline):
    model = OrderAddress
    can_delete = False
    verbose_name_plural = 'Shipping Address'
    fields = ('fullname', 'phone', 'address_line', 'ward', 'district', 'province')

class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0
    fields = ('payment_method', 'amount', 'status', 'transaction_id', 'paid_at')
    readonly_fields = ('paid_at',)

class FulfillmentInline(admin.TabularInline):
    model = Fulfillment
    extra = 0
    fields = ('tracking_number', 'shipping_carrier', 'status', 'shipped_at', 'delivered_at')
    readonly_fields = ('shipped_at', 'delivered_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'subtotal_amount', 'tax_amount', 'shipping_fee', 'final_total_amount', 'created_at')
    list_filter = ('status', "created_at")
    search_fields = ('id', 'user__username')
    readonly_fields = ('id', )
    inlines = [OrderItemInline, PaymentTransactionInline, FulfillmentInline, OrderAddressInline]
