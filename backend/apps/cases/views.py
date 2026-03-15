from rest_framework import mixins, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .models import Case, CaseRecord
from .serializers import CaseRecordSerializer, CaseSerializer

ALLOWED_MIME_TYPES = {"text/plain", "application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class CaseViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Cases are create-only (POST + GET).
    Update and delete are intentionally excluded.
    """

    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
                "count": queryset.count(),
            }
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"success": True, "data": serializer.data})


class CaseRecordUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, case_id):
        case = get_object_or_404(Case, pk=case_id)

        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "validation_error",
                        "message": "No file was provided. Include a 'file' field in the multipart request.",
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        mime_type = uploaded_file.content_type
        if mime_type not in ALLOWED_MIME_TYPES:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "validation_error",
                        "message": (
                            f"Unsupported file type '{mime_type}'. "
                            "Only text/plain and application/pdf are allowed."
                        ),
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_size = uploaded_file.size
        if file_size == 0:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "validation_error",
                        "message": "The uploaded file is empty (0 bytes). Please upload a non-empty file.",
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if file_size > MAX_FILE_SIZE:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "validation_error",
                        "message": (
                            f"File size {file_size} bytes exceeds the 10 MB limit "
                            f"({MAX_FILE_SIZE} bytes)."
                        ),
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        record = CaseRecord.objects.create(
            case=case,
            file=uploaded_file,
            original_filename=uploaded_file.name,
            mime_type=mime_type,
            file_size=file_size,
        )

        serializer = CaseRecordSerializer(record)
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
