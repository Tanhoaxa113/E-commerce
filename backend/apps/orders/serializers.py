from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    render_status = serializers.ReadOnlyField()
    # status_text = serializers.CharField(source='get_status_display', read_only=True) #Dùng khi render TEXT, không cần dùng @property trong model
    class Meta:
        model = Order
        fields = [
            'id',
            'code',
            'status',
            'render_status',
            'final_total_amount',
        ]