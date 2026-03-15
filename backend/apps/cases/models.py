from django.db import models

from apps.patients.models import Patient
from apps.providers.models import Provider


class Case(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="cases",
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cases",
    )
    primary_diagnosis = models.CharField(max_length=20)
    medications = models.JSONField(default=list)
    notes = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Case"

    def __str__(self) -> str:
        return f"Case #{self.pk} – {self.patient} [{self.status}]"


class CaseRecord(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="records")
    file = models.FileField(upload_to="case_records/%Y/%m/")
    original_filename = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    file_size = models.PositiveIntegerField()  # bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "CaseRecord"

    def __str__(self) -> str:
        return f"CaseRecord #{self.pk} – {self.original_filename} ({self.case})"
