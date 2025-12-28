from .models import CustomUser, Staff
from rest_framework import generics
from .serializers import UserSerializer, TwoFactorSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status, response, request
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse
from django.db import transaction
from django.utils import timezone
from .tasks import send_otp_to_email

class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        
        return Response({
            "message": "Đăng ký thành công!",
            "user": serializer.data,
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            a = timezone.now()
            print("Vào khối try", a)
            serializer.is_valid(raise_exception=True)
            user = CustomUser.objects.get(username=request.data.get('username'))
            send_otp_to_email.delay(user.id)
            b = timezone.now() - a
            print("Kết thúc khối try",b)
            return Response({
                "message": "Đăng nhập hợp lệ! OTP đã được gửi đến email của bạn.",
                
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"message": "Tài khoản không tồn tại!"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({"message": "Dữ liệu không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Đã có lỗi xảy ra!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TwoFactorView(TokenObtainPairView):
    serializer_class = TwoFactorSerializer

    def post(self, request, *args,):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(username=request.data.get('username'))
        if not user:
            return Response({"message": "Lỗi không tìm thấy user",})
        else:
            response = Response({"message": "Đăng nhập thành công"}, status=status.HTTP_200_OK)
            access_token = serializer.validated_data.get('access')
            response.set_cookie('access_token',access_token, max_age=None, expires=None, secure=True, httponly=True, samesite='Lax')
            return response

class LogoutView(generics.GenericAPIView):
    erializer_class = CustomTokenObtainPairSerializer
    def post(self, request):
        response = Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        return response