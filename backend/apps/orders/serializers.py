from rest_framework import serializers
from .models import Order, OrderItem, OrderAddress
from apps.products.models import ProductVariant, ProductStock
from django.db import transaction

class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = ['fullname', 'phone', 'address_line', 'ward', 'district', 'province']

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField() 

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price', 'total_line_amount']
        read_only_fields = ['price', 'total_line_amount']

class OrderSerializer(serializers.ModelSerializer):
    shipping_address = OrderAddressSerializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'code', 'user', 'status', 'shipping_address', 'items', 
            'subtotal_amount', 'tax_amount', 'shipping_fee', 
            'coupon', 'discounted_amount', 'tier_discount_amount',
            'final_total_amount', 'order_note', 'created_at'
        ]
        read_only_fields = [
            'id', 'code', 'user', 'status', 'created_at',
            'subtotal_amount', 'tax_amount', 'final_total_amount', 
            'discounted_amount', 'tier_discount_amount'
        ]

    def create(self, validated_data):
        address_data = validated_data.pop('shipping_address')
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(user=user, **validated_data)
            OrderAddress.objects.create(order=order, **address_data)
            total_bill = 0
            
            for item_data in items_data:
                product_id = item_data['product_id']
                quantity = item_data['quantity']

                try:
                    product = ProductVariant.objects.get(id=product_id)
                except ProductVariant.DoesNotExist:
                    raise serializers.ValidationError({"items": f"Sản phẩm ID {product_id} không tồn tại."})
                if ProductStock.objects.get(variant=product).quantity < quantity:
                    raise serializers.ValidationError({"items": f"Sản phẩm {product.name} không đủ hàng."})

                line_amount = product.price * quantity
                total_bill += line_amount

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                    total_line_amount=line_amount
                )

            order.subtotal_amount = total_bill
            order.final_total_amount = total_bill + order.shipping_fee - order.discounted_amount
            order.save()
            
            return order