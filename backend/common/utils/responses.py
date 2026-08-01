"""
Standard API response envelope used by every WEBTECH endpoint.

Success: {"success": true, "message": "...", "data": {...}}
Error:   {"success": false, "message": "...", "errors": {...}}
"""
from rest_framework.response import Response


def success_response(data=None, message="OK", status=200):
    return Response({"success": True, "message": message, "data": data}, status=status)


def error_response(errors=None, message="Something went wrong", status=400):
    return Response({"success": False, "message": message, "errors": errors}, status=status)
