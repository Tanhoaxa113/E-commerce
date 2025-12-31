from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from django.db import transaction

from .models import Order
from .serializers import OrderSerializer
from .tasks import process_order_task

class OrderViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.save()

        transaction.on_commit(lambda: process_order_task.delay(order.id))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)