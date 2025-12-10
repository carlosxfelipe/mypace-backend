from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # Busca o usuário pelo email
            try:
                user = User.objects.get(email=email)
                # Autentica usando o username
                user = authenticate(
                    request=self.context.get("request"),
                    username=user.username,
                    password=password,
                )
            except User.DoesNotExist:
                user = None

            if not user:
                msg = "Impossível fazer login com as credenciais fornecidas."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'É necessário fornecer "email" e "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "password", "password_confirm", "first_name", "last_name"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        # Usa o email como username
        validated_data["username"] = validated_data["email"]
        user = User.objects.create_user(**validated_data)
        return user
