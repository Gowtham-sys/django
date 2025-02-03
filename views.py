from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
import random

from .models import CustomUser, OTP
from .serializers import (
    UserRegistrationSerializer,
    OTPVerificationSerializer,
    LoginSerializer,
    UserSerializer
)

class HelloAPI(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({"message": "API working!"})


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user and send OTP via email"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)  # User is inactive until OTP verification
            
            # Generate and save OTP
            otp_code = random.randint(100000, 999999)
            OTP.objects.create(user=user, code=otp_code, expires_at=timezone.now() + timezone.timedelta(minutes=5))

            # Send OTP via email
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is {otp_code}. It expires in 5 minutes.",
                from_email="your-email@gmail.com",
                recipient_list=[user.email],
            )

            return Response({'detail': 'OTP sent to email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Verify OTP and activate the user"""
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            try:
                user = CustomUser.objects.get(email=email)
                otp = OTP.objects.filter(user=user).latest('created_at')
            except (CustomUser.DoesNotExist, OTP.DoesNotExist):
                return Response({'detail': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if OTP is expired or incorrect
            if otp.expires_at < timezone.now() or otp.code != code:
                return Response({'detail': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

            # Activate user
            user.is_active = True
            user.save()

            return Response({'detail': 'User activated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Login user and return JWT tokens"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )

            if user and user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                })
            
            return Response({'detail': 'Invalid credentials or account not activated'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve authenticated user details"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Verify email using a token (Optional, not OTP-based)"""
        token = request.GET.get('token')

        # Here, implement logic to verify the email using the token (if needed)

        return Response({"status": "Email verified"}, status=200)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout user by blacklisting JWT token"""
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

