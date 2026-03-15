from django.core.validators import RegexValidator
from django.db import models


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    mrn = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message="MRN must be exactly 8 digits.",
            )
        ],
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    phone = models.CharField(max_length=30, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Patient"
        indexes = [
            models.Index(fields=["mrn"], name="patient_mrn_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name} (MRN: {self.mrn})"
