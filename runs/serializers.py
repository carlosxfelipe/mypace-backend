from rest_framework import serializers
from .models import Run


class RunSerializer(serializers.ModelSerializer):
    pace = serializers.ReadOnlyField()

    class Meta:
        model = Run
        fields = [
            "id",
            "date",
            "distance_km",
            "time_minutes",
            "pace",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        # Adiciona o usuário automaticamente
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
