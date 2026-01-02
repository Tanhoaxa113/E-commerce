from .models import CustomUser, Staff
from rest_framework import generics
from .serializers import UserSerializer, TwoFactorSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.db import transaction
from django.utils import timezone
from .tasks import send_otp_to_email
from django.db.models import Q
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
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            a = timezone.now()
            print("Vào khối try", a)
            
            user = CustomUser.objects.get(Q(username=request.data.get('username')) |Q(email=request.data.get('username')))
            send_otp_to_email.delay(user.id)
            b = timezone.now() - a
            print("Kết thúc khối try",b)
            return Response({
                "message": "Đăng nhập hợp lệ! OTP đã được gửi đến email của bạn.",
                "required_otp" : True,
                "user_id": user.id,
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
        user = CustomUser.objects.get(Q(username=request.data.get('username')) |Q(email=request.data.get('username')))
        if not user:
            return Response({"message": "Lỗi không tìm thấy user",})
        else:
            access_token = serializer.validated_data.get('access')
            refresh_token = serializer.validated_data.get('refresh')
            response_data = {
                "message": "Đăng nhập thành công",
                "refresh_token": refresh_token,
                "user_id": user.id,
                
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                max_age=3600,
                samesite='Lax',
                secure=False,
                path='/'
            )
            return response

class LogoutView(generics.GenericAPIView):
    erializer_class = CustomTokenObtainPairSerializer
    def post(self, request):
        response = Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        return response