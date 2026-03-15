import re

from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "mrn",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_mrn(self, value):
        if not re.fullmatch(r"\d{8}", value):
            raise serializers.ValidationError(
                "MRN must be exactly 8 digits (0-9)."
            )
        return value
