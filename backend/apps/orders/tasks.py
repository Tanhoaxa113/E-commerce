from celery import shared_task
from django.db import transaction
from django.db.models import F
from .models import Order
from apps.products.models import ProductVariant, ProductStock
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
logger = logging.getLogger(__name__)

@shared_task
def process_order_task(order_id):
    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=order_id)
            if order.status != Order.OrderStatus.PENDING:
                logger.warning(f"Đơn {order.code} không ở trạng thái PENDING. Bỏ qua.")
                return
            order.start_processing()
            order.save()
            for item in order.items.all():
                variant = item.product
                needed_qty = item.quantity

                stock_record = ProductStock.objects.select_for_update().filter(
                    variant=variant,
                    quantity__gte=needed_qty
                ).first()

                if stock_record:
                    stock_record.quantity = F('quantity') - needed_qty
                    stock_record.save()
                else:
                    raise Exception(f"Sản phẩm {variant.name} ({variant.sku}) đã hết hàng trên toàn hệ thống.")
            order.processing_passed()
            order.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{order.user.id}", # Tên group phải khớp với bên Consumer
                {
                    "type": "order_status_update", # Tên hàm trong Consumer xử lý
                    "message": f"Đơn hàng {order.code} đã được xác nhận!",
                    "data": {
                        "order_id": str(order.id),
                        "status": order.status,
                        "code": order.code
                    }
                }
            )
            logger.info(f"✅ Đơn {order.code} xử lý thành công!")

    except Exception as e:
        logger.error(f"❌ Lỗi xử lý đơn {order_id}: {e}")
        mark_order_failed.delay(order_id, str(e))

@shared_task
def mark_order_failed(order_id, error_msg):
    try:
        order = Order.objects.get(id=order_id)
        if order.status in [Order.OrderStatus.PENDING, Order.OrderStatus.PROCESSING]:
            order.processing_failed(note=error_msg)
            order.save()
    except Exception as e:
        logger.error(f"Không thể update status Failed: {e}")