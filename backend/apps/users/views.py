from .models import CustomUser, Staff
from rest_framework import generics
from .serializers import UserSerializer, TwoFactorSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.db import transaction
from django.utils import timezone
from .tasks import send_otp_to_email
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
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
            avatar_url = None
            gender = None
            phone_number = None
            address = None
            customer_type = None
            loyalty_points = None
            position = None
            work_address = None
            hire_date = None
            try:
                profile = getattr(user, 'profile', None)
                staff = getattr(user, 'staff', None)
                if profile:
                    gender = profile.gender
                    phone_number = profile.phone_number
                    address = profile.address
                    customer_type = profile.customer_type
                    loyalty_points = profile.loyalty_points
                if profile.avatar:
                    avatar_url = profile.avatar.url
                if staff:
                    position = staff.position
                    work_address = staff.work_address
                    hire_date = staff.hire_date
            except Exception as e:
                avatar_url = None

            access_token = serializer.validated_data.get('access')
            refresh_token = serializer.validated_data.get('refresh')
            response_data = {
                "message": "Đăng nhập thành công",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "avatar": avatar_url,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "gender": gender,
                "phone_number": phone_number,
                "address": address,
                "customer_type": customer_type,
                "loyalty_points": loyalty_points,
                "position": position,
                "work_address": work_address,
                "hire_date": hire_date,
                
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
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                max_age=24 * 7 * 60 * 60,
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

class TokenRefreshViewWithCookie(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            raise AuthenticationFailed('Không tìm thấy Refresh Token trong Cookie')
        data = {'refresh': refresh_token}
        serializer = self.get_serializer(data=data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            raise AuthenticationFailed('Refresh Token hết hạn hoặc không hợp lệ')
        new_access_token = serializer.validated_data.get('access')
        response = Response({'message': 'Refreshed success'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )
        
        return response
    
class GetMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user