"""
S18: Standardized error envelope for all API responses.

All errors return:
{
    "success": false,
    "error": {
        "code": "<error_code>",
        "message": "<safe non-technical message>",
        "details": { ... }   // optional field-level errors
    }
}
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "internal_error",
                    "message": "An unexpected error occurred. Please try again.",
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    error_payload = {
        "success": False,
        "error": {
            "code": _resolve_code(response.status_code),
            "message": _resolve_message(response.data, response.status_code),
        },
    }

    # Preserve field-level validation details
    if isinstance(response.data, dict) and response.status_code == 400:
        field_errors = {
            k: v for k, v in response.data.items()
            if k not in ("detail", "non_field_errors")
        }
        if field_errors:
            error_payload["error"]["details"] = field_errors
        non_field = response.data.get("non_field_errors")
        if non_field:
            error_payload["error"]["message"] = (
                non_field[0] if isinstance(non_field, list) else str(non_field)
            )

    response.data = error_payload
    return response


def _resolve_code(status_code: int) -> str:
    mapping = {
        400: "validation_error",
        401: "authentication_required",
        403: "permission_denied",
        404: "not_found",
        405: "method_not_allowed",
        409: "conflict",
        429: "rate_limit_exceeded",
        500: "internal_error",
    }
    return mapping.get(status_code, f"http_{status_code}")


def _resolve_message(data, status_code: int) -> str:
    if isinstance(data, dict):
        detail = data.get("detail")
        if detail:
            return str(detail)
    if isinstance(data, list) and data:
        return str(data[0])
    default_messages = {
        400: "Request data is invalid.",
        401: "Authentication is required.",
        403: "You do not have permission to perform this action.",
        404: "The requested resource was not found.",
        409: "A conflict occurred with the current state of the resource.",
    }
    return default_messages.get(status_code, "An error occurred.")
