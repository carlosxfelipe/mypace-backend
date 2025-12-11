from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.db.models import Count, Sum, Avg, Min, F
from .models import Run
from .serializers import (
    RunSerializer,
    EmailAuthTokenSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )


class EmailAuthToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(
            {"message": "Conta deletada com sucesso."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Invalida o token atual e cria um novo
        Token.objects.filter(user=request.user).delete()
        token = Token.objects.create(user=request.user)
        return Response(
            {
                "message": "Senha alterada com sucesso.",
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )


class RunViewSet(viewsets.ModelViewSet):
    serializer_class = RunSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas as corridas do usuário logado
        return Run.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """Retorna estatísticas das corridas do usuário"""
        runs = self.get_queryset()

        stats = runs.aggregate(
            total_runs=Count("id"),
            total_distance=Sum("distance_km"),
            avg_pace=Avg(F("time_minutes") / F("distance_km")),
            best_pace=Min(F("time_minutes") / F("distance_km")),
        )

        return Response(stats)
