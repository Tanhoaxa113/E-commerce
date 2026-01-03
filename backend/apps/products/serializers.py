from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'price', 'variant_specs', 'discount_rate', 'final_price', 'images'] #fields của variant cần nhúng vào product

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True) #nhúng variants vào product
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    videos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'description', 'variants', 'comments', 'videos', 'reviews']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']
    
class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ['id', 'thumbnail','duration', 'hls_url']

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['id', 'user', 'comment', 'created_at']
