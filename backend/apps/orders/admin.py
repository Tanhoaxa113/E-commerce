from django.contrib import admin
from .models import *
from django_fsm import TransitionNotAllowed

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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

    readonly_fields = ['status','id',]
    actions = ['admin_confirm', 'admin_start_delivery', 'admin_complete', 'admin_cancel']

    @admin.action(description='Duyệt/Xác nhận đơn (Confirm)')
    def admin_confirm(self, request, queryset):
        self._apply_transition(request, queryset, 'confirm', 'Đã xác nhận')

    @admin.action(description='Cho đi giao hàng (Start Delivering)')
    def admin_start_delivery(self, request, queryset):
        self._apply_transition(request, queryset, 'start_delivering', 'Đang giao')

    @admin.action(description='Đánh dấu Hoàn thành (Complete)')
    def admin_complete(self, request, queryset):
        self._apply_transition(request, queryset, 'complete', 'Hoàn thành')

    @admin.action(description='Hủy đơn hàng (Cancel)')
    def admin_cancel(self, request, queryset):
        self._apply_transition(request, queryset, 'cancel', 'Đã hủy')

    def _apply_transition(self, request, queryset, method_name, status_display):
        success = 0
        failed = 0
        channel_layer = get_channel_layer()
        for order in queryset:
            try:
                transition_func = getattr(order, method_name)
                transition_func()
                order.save()

                async_to_sync(channel_layer.group_send)(
                    f"user_{order.user.id}", # Tên group phải khớp với bên Consumer
                    {
                        "type": "order_status_update", # Tên hàm trong Consumer xử lý
                        "message": f"Đơn hàng {order.code} đã chuyển trạng thái",
                        "data": {
                            "order_id": str(order.id),
                            "status": order.status,
                            "code": order.code
                        }
                    }
                )
                success += 1
            except TransitionNotAllowed:
                failed += 1
            except Exception as e:
                self.message_user(request, f"Lỗi đơn {order.code}: {e}", level='error')
        if success:
            self.message_user(request, f"Đã chuyển {success} đơn sang '{status_display}'.", level='success')
        if failed:
            self.message_user(request, f"Có {failed} đơn không thể chuyển trạng thái (sai quy trình).", level='warning')
    inlines = [OrderItemInline, FulfillmentInline, OrderAddressInline]


    