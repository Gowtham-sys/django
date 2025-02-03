from django.urls import path
from .views import (
    HelloAPI, 
    UserRegistrationView, 
    OTPVerificationView, 
    LoginView, 
    UserDetailsView, 
    LogoutView, 
    VerifyEmailView
)

urlpatterns = [
    path('', HelloAPI.as_view(), name='hello_api'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('register/verify/', OTPVerificationView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserDetailsView.as_view(), name='user_details'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]
