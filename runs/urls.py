from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RunViewSet,
    EmailAuthToken,
    RegisterView,
    DeleteAccountView,
    ChangePasswordView,
)

router = DefaultRouter()
router.register(r"runs", RunViewSet, basename="run")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", EmailAuthToken.as_view(), name="email-login"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("auth/delete-account/", DeleteAccountView.as_view(), name="delete-account"),
]
