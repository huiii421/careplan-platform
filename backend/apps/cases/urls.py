from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CaseRecordUploadView, CaseViewSet

router = DefaultRouter()
router.register(r"cases", CaseViewSet, basename="case")

urlpatterns = router.urls + [
    path("cases/<int:case_id>/records/", CaseRecordUploadView.as_view(), name="case-record-upload"),
]
