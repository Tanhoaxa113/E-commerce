from .models import *
from rest_framework import serializers

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'price', 'color', 'specifications'] #fields của variant cần nhúng vào product

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True) #nhúng variants vào product

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'variants']
    