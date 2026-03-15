from rest_framework import serializers

from apps.core.validators import validate_icd10
from apps.patients.models import Patient
from apps.providers.models import Provider

from .models import Case, CaseRecord


class CaseSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    provider = serializers.PrimaryKeyRelatedField(
        queryset=Provider.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Case
        fields = [
            "id",
            "patient",
            "provider",
            "primary_diagnosis",
            "medications",
            "notes",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_primary_diagnosis(self, value):
        validate_icd10(value)
        return value

    def validate_medications(self, value):
        if not isinstance(value, list) or len(value) == 0:
            raise serializers.ValidationError(
                "medications must be a non-empty list."
            )
        return value

    def validate(self, data):
        from apps.core.rules import apply_rules

        rules = [
            # Rule 1: primary_diagnosis must be present and non-empty.
            (
                lambda d: not d.get("primary_diagnosis"),
                "primary_diagnosis",
                "primary_diagnosis is required and must not be empty.",
            ),
            # Rule 2: medications must be a non-empty list.
            (
                lambda d: not isinstance(d.get("medications"), list)
                or len(d.get("medications", [])) == 0,
                "medications",
                "medications must be a non-empty list.",
            ),
            # Rule 3: if provider is supplied, primary_diagnosis must be present.
            (
                lambda d: d.get("provider") is not None
                and not d.get("primary_diagnosis"),
                "primary_diagnosis",
                "Required when provider is specified.",
            ),
            # Rule 4: every medication item must be a non-empty string.
            (
                lambda d: isinstance(d.get("medications"), list)
                and any(
                    not isinstance(item, str) or not item.strip()
                    for item in d.get("medications", [])
                ),
                "medications",
                "Medication items must be non-empty strings.",
            ),
            # Rule 5: medications list must not exceed 50 items.
            (
                lambda d: isinstance(d.get("medications"), list)
                and len(d.get("medications", [])) > 50,
                "medications",
                "medications must not exceed 50 items.",
            ),
        ]

        apply_rules(data, rules)
        return data


class CaseRecordSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = CaseRecord
        fields = [
            "id",
            "case",
            "file",
            "original_filename",
            "mime_type",
            "file_size",
            "uploaded_at",
        ]
        read_only_fields = ["id", "case", "original_filename", "mime_type", "file_size", "uploaded_at"]
