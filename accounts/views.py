from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from.models import UserProfile
from django.core.mail import EmailMultiAlternatives
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = serializer.save()

        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verify_url = f"http://localhost:5173/verify/{uid}/{token}/"

        subject = "Verify your TuneFlow Account 🎧"

        text_content = f"Hi {user.name}, Please verify your account: {verify_url}"

        html_content = f"""
        <div style="font-family: Arial; padding: 20px;">
          <h2 style="color: purple;">Welcome to TuneFlow 🎧</h2>

          <p>Hi {user.name},</p>

          <p>Thanks for signing up! Please verify your email to activate your account.</p>

          <a href="{verify_url}" 
             style="display:inline-block; padding:10px 20px; background:purple; color:white; text-decoration:none; border-radius:5px;">
             Verify Email
          </a>

          <p style="margin-top:20px;">If you didn’t create this account, ignore this email.</p>

          <p>— TuneFlow Team 🚀</p>
        </div>
        """

        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [user.email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({"message": "Check your email to verify account"})
    

class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = UserProfile.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Email verified"})
            return Response({"error": "Invalid token"}, status=400)

        except:
            return Response({"error": "Invalid link"}, status=400)
        


class LoginView(APIView):

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        try:
            
            email = request.data.get("email")
            password = request.data.get("password")
            
            
            user_obj = User.objects.filter(email=email).first()

            if not user_obj:
                return Response({"error": "User not found"}, status=400)
            if not user_obj.is_active:
                return Response({"error": "Please verify your email first"}, status=403)
            user = authenticate(email=email, password=password)
            if not user:
                return Response({"error": "Invalid credentials"}, status=400)
            
            if user.status.lower() != "active":
                return Response({"error": "Account is blocked"}, status=403)
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "name": user.name,
                    "email": user.email,
                    "role": user.role 
                }
            })

        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = UserProfile.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            verify_url = f"http://localhost:5173/reset/{uid}/{token}/"

            subject = "Verify your TuneFlow Account 🎧"

            text_content = f"Hi {user.name}, Please verify your account: {verify_url}"

            html_content = f"""
            <div style="font-family: Arial; padding: 20px;">
            <h2 style="color: purple;">Welcome to TuneFlow 🎧</h2>

            <p>Hi {user.name},</p>

            <p>Thanks for signing up! Please verify your email to activate your account.</p>

            <a href="{verify_url}" 
                style="display:inline-block; padding:10px 20px; background:purple; color:white; text-decoration:none; border-radius:5px;">
                Verify Email
            </a>

            <p style="margin-top:20px;">If you didn’t create this account, ignore this email.</p>

            <p>— TuneFlow Team 🚀</p>
            </div>
            """

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Reset link sent"})

        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        

class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = UserProfile.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid token"}, status=400)

            password = request.data.get("password")
            user.set_password(password)
            user.save()

            return Response({"message": "Password reset successful"})

        except:
            return Response({"error": "Something went wrong"}, status=400)
        


class ResendVerificationView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = UserProfile.objects.get(email=email)

            if user.is_active:
                return Response({"message": "Already verified"})

            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            from django.contrib.auth.tokens import default_token_generator
            from django.core.mail import send_mail
            from django.conf import settings

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            verify_url = f"http://localhost:5173/verify/{uid}/{token}/"

            subject = "Verify your TuneFlow Account 🎧"

            text_content = f"Hi {user.name}, Please verify your account: {verify_url}"

            html_content = f"""
            <div style="font-family: Arial; padding: 20px;">
            <h2 style="color: purple;">Welcome to TuneFlow 🎧</h2>

            <p>Hi {user.name},</p>

            <p>Thanks for signing up! Please verify your email to activate your account.</p>

            <a href="{verify_url}" 
                style="display:inline-block; padding:10px 20px; background:purple; color:white; text-decoration:none; border-radius:5px;">
                Verify Email
            </a>

            <p style="margin-top:20px;">If you didn’t create this account, ignore this email.</p>

            <p>— TuneFlow Team 🚀</p>
            </div>
            """

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Email resent"})

        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        