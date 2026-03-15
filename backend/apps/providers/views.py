from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Provider
from .serializers import ProviderSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def create(self, request, *args, **kwargs):
        npi = request.data.get("npi")

        # Upsert-by-NPI: return existing provider if NPI already exists.
        if npi:
            try:
                existing = Provider.objects.get(npi=npi)
                serializer = self.get_serializer(existing)
                return Response(
                    {"success": True, "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            except Provider.DoesNotExist:
                pass

        # NPI not found — create a new provider.
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
