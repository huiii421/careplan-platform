from django.core.validators import RegexValidator
from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=255)
    npi = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="NPI must be exactly 10 digits.",
            )
        ],
    )
    specialty = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Provider"
        indexes = [
            models.Index(fields=["npi"], name="provider_npi_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.name} (NPI: {self.npi})"
