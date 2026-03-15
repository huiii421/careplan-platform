from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    """S1: Health check endpoint. Returns 200 with service status."""
    return Response({"success": True, "status": "ok", "service": "careplan-platform"})
