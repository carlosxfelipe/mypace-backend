from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg, Min, F
from .models import Run
from .serializers import RunSerializer


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
