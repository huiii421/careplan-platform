import re

from rest_framework import serializers

from .models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            "id",
            "name",
            "npi",
            "specialty",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_npi(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise serializers.ValidationError(
                "NPI must be exactly 10 digits (0-9)."
            )
        return value
