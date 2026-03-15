"""
ICD-10 validator service.

Provides a reusable validate_icd10() function that:
1. Checks code format via regex.
2. Checks the code against a local dictionary of ~50 common codes.

Importable from: apps.core.validators
"""

import re

from rest_framework import serializers

# ---------------------------------------------------------------------------
# Regex pattern
# ---------------------------------------------------------------------------
ICD10_PATTERN = re.compile(r"^[A-Z][0-9]{2}(\.[0-9A-Z]{1,4})?$")

# ---------------------------------------------------------------------------
# Local dictionary of ~50 common ICD-10 codes covering major categories
# ---------------------------------------------------------------------------
KNOWN_ICD10_CODES: frozenset = frozenset(
    {
        # A00-B99  Infectious & parasitic diseases
        "A09",    # Infectious gastroenteritis
        "A41.9",  # Sepsis, unspecified
        "B20",    # HIV disease
        "B34.9",  # Viral infection, unspecified
        # C00-D49  Neoplasms
        "C34.1",  # Malignant neoplasm of upper lobe, bronchus or lung
        "C50.9",  # Malignant neoplasm of breast, unspecified
        "C18.9",  # Malignant neoplasm of colon, unspecified
        "C61",    # Malignant neoplasm of prostate
        "D64.9",  # Anaemia, unspecified
        # E00-E89  Endocrine, nutritional & metabolic diseases
        "E11.9",  # Type 2 diabetes mellitus without complications
        "E11.65", # Type 2 diabetes mellitus with hyperglycemia
        "E10.9",  # Type 1 diabetes mellitus without complications
        "E78.5",  # Hyperlipidaemia, unspecified
        "E66.9",  # Obesity, unspecified
        "E03.9",  # Hypothyroidism, unspecified
        # F01-F99  Mental, behavioural & neurodevelopmental disorders
        "F32.9",  # Major depressive disorder, single episode, unspecified
        "F41.1",  # Generalised anxiety disorder
        "F10.20", # Alcohol use disorder, moderate
        "F20.9",  # Schizophrenia, unspecified
        "F31.9",  # Bipolar disorder, unspecified
        # G00-G99  Nervous system
        "G20",    # Parkinson's disease
        "G30.9",  # Alzheimer's disease, unspecified
        "G40.909",# Epilepsy, unspecified, not intractable
        "G43.909",# Migraine, unspecified, not intractable
        # I00-I99  Circulatory system
        "I10",    # Essential (primary) hypertension
        "I25.10", # Atherosclerotic heart disease
        "I48.91", # Unspecified atrial fibrillation
        "I50.9",  # Heart failure, unspecified
        "I63.9",  # Cerebral infarction, unspecified
        "I21.9",  # Acute myocardial infarction, unspecified
        # J00-J99  Respiratory system
        "J06.9",  # Acute upper respiratory infection, unspecified
        "J18.9",  # Pneumonia, unspecified
        "J44.1",  # Chronic obstructive pulmonary disease with acute exacerbation
        "J45.909",# Unspecified asthma, uncomplicated
        # K00-K95  Digestive system
        "K21.0",  # Gastro-oesophageal reflux disease with oesophagitis
        "K57.30", # Diverticulosis of large intestine without perforation
        "K92.1",  # Melaena
        "K70.30", # Alcoholic cirrhosis of liver without ascites
        # M00-M99  Musculoskeletal & connective tissue
        "M06.9",  # Rheumatoid arthritis, unspecified
        "M17.11", # Primary osteoarthritis, right knee
        "M54.5",  # Low back pain
        "M79.3",  # Panniculitis
        # N00-N99  Genitourinary system
        "N18.3",  # Chronic kidney disease, stage 3
        "N39.0",  # Urinary tract infection, site not specified
        "N40.1",  # Benign prostatic hyperplasia with lower urinary tract symptoms
        "N17.9",  # Acute kidney failure, unspecified
        # Z00-Z99  Factors influencing health status
        "Z00.00", # Encounter for general adult medical examination without abnormal findings
        "Z12.31", # Encounter for screening mammogram for malignant neoplasm of breast
        "Z23",    # Encounter for immunization
        "Z51.11", # Encounter for antineoplastic chemotherapy
        "Z87.891",# Personal history of nicotine dependence
    }
)


# ---------------------------------------------------------------------------
# Public validator function
# ---------------------------------------------------------------------------
def validate_icd10(code: str) -> None:
    """
    Validate an ICD-10 diagnosis code.

    Steps:
    1. Check format with ICD10_PATTERN regex.
    2. Check against KNOWN_ICD10_CODES dictionary.

    Raises:
        rest_framework.serializers.ValidationError on failure.
    """
    if not ICD10_PATTERN.match(code):
        raise serializers.ValidationError(
            "Invalid ICD-10 format: must be like A01 or B20.1"
        )
    if code not in KNOWN_ICD10_CODES:
        raise serializers.ValidationError(
            f"ICD-10 code '{code}' is not recognized. Verify the diagnosis code."
        )
