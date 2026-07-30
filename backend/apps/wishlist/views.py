"""
Views for the wishlist app.

Purpose: User wishlists and wishlist items.

Views only: parse request -> call serializer -> call service -> return
standard {success, message, data} / {success, message, errors} response.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# TODO: Implement wishlist views here, using the standard WEBTECH API
# response envelope (see common/utils/responses.py).
