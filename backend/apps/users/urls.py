from django.urls import path, include
from django.conf import settings
from .views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginView, TwoFactorView, LogoutView


urlpatterns = [
    path('register/', CreateUserView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name="login"),
    path('login/2fa/', TwoFactorView.as_view(), name="2fa"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
    
]

