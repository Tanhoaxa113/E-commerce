from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .models import Order, OrderItem

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    order_items_aggregation = order.items.aggregate(
        subtotal=Sum('total_line_amount')
    )
    item_total = order_items_aggregation['subtotal'] or 0

    tax_aggregation = order.items.aggregate(
        total_tax=Sum(
            F('total_line_amount') * F('product__product__tax_rate') / 100,
            output_field=DecimalField()
        )
    )

    tax_total = tax_aggregation['total_tax'] or 0
    order.subtotal_amount = item_total
    order.tax_amount = tax_total

    order.final_total_amount = (
        order.subtotal_amount +
        order.tax_amount +
        order.shipping_fee -
        order.discounted_amount -
        order.tier_discount_amount
    )

    order.save(update_fields=['subtotal_amount', 'tax_amount', 'final_total_amount'])