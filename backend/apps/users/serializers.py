from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['id'] = self.user.id

        return data

class TwoFactorSerializer(TokenObtainPairSerializer):
    otp = serializers.CharField(max_length=8)
    username = serializers.CharField(max_length=150)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('username')
        otp = attrs.get('otp')

        if not username or not otp:
            raise serializers.ValidationError("Phải cung cấp tên người dùng và OTP.")

        try:
            user = CustomUser.objects.get(Q(email=email) | Q( username=username))
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Người dùng không tồn tại.")

        if not user.otp or user.otp != otp:
            raise serializers.ValidationError("Mã OTP không hợp lệ.")

        if user.otp_valid_until and timezone.now() > user.otp_valid_until:
            raise serializers.ValidationError("Mã OTP đã hết hạn.")
        
        user.otp = None
        user.otp_valid_until = None
        data = super().validate(attrs)
        data['username'] = user.username
        data['email'] = user.email
        data['id'] = user.id
        user.invalid_try = 0
        user.save()

        self.user = user
        return data
