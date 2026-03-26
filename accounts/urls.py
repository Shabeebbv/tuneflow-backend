from django.urls import path
from .views import RegisterView, LoginView,VerifyEmailView,ForgotPasswordView,ResetPasswordView,ResendVerificationView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
     path("verify/<uid>/<token>/", VerifyEmailView.as_view()),
     path("forgot-password/", ForgotPasswordView.as_view()),
     path("reset/<uid>/<token>/", ResetPasswordView.as_view()),
     path("resend-verification/", ResendVerificationView.as_view()),
]