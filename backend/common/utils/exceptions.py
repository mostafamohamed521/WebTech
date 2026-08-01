"""
Central DRF exception handler so every error follows the WEBTECH
standard error envelope instead of DRF's default format.
"""
from rest_framework.views import exception_handler
from .responses import error_response


def webtech_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return error_response(errors=response.data, message="Request failed", status=response.status_code)
    return response
