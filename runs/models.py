from django.db import models
from django.contrib.auth.models import User
import uuid


class Run(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="runs")
    date = models.DateTimeField()
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    time_minutes = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "-date"]),
        ]

    @property
    def pace(self):
        """Calcula o pace em min/km"""
        if self.distance_km > 0:
            return float(self.time_minutes / self.distance_km)
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.date.date()} - {self.distance_km}km"
